#!/usr/bin/env python3
"""
B-Score（量化版）计算脚本
输入：财务数据字典（通过命令行参数）
输出：量化B-Score各项得分及总分（JSON格式）
"""

import argparse
import json
import sys
import statistics


def calc_b_score_quant(data: dict) -> dict:
    """
    计算量化版B-Score（满分10分）
    
    data 字段说明：
    - net_incomes: 近5年净利润列表 [y-4, y-3, y-2, y-1, y0]
    - operating_cfs: 近3年经营现金流列表 [y-2, y-1, y0]
    - capexs: 近3年资本支出列表 [y-2, y-1, y0]
    - gross_margin_latest: 最新年度毛利率 (小数，如0.35)
    - roes: 近3年ROE列表 (小数，如0.12)
    - debt_ratio: 最新年度资产负债率 (小数，如0.45)
    - dividend_yields: 近3年股息率列表 (小数，如0.035)
    - has_high_premium_ma: 近5年是否有高溢价并购(溢价率>50%) (bool)
    - has_frequent_issuance: 近5年是否有频繁增发(≥2次) (bool)
    - financing_mismatch: 融资用途是否与承诺严重不符 (bool)
    """
    
    results = {}
    total = 0
    
    # ===== 1. 盈利能力真实性（3分）=====
    
    # 1.1 净利润稳定性（1分）
    net_incomes = data['net_incomes']
    all_positive = all(ni > 0 for ni in net_incomes)
    if all_positive:
        mean_ni = statistics.mean(net_incomes)
        std_ni = statistics.stdev(net_incomes) if len(net_incomes) > 1 else 0
        cv = std_ni / abs(mean_ni) if mean_ni != 0 else float('inf')
        if cv < 0.3:
            results['profit_stability'] = 1.0
        elif cv < 0.6:
            results['profit_stability'] = 0.5
        else:
            results['profit_stability'] = 0
    else:
        results['profit_stability'] = 0
        cv = None
    results['profit_stability_cv'] = cv
    total += results['profit_stability']
    
    # 1.2 现金流质量（1分）
    cfs = data['operating_cfs']
    nis_last3 = data['net_incomes'][-3:]
    cf_ratios = [cf / ni if ni > 0 else 0 for cf, ni in zip(cfs, nis_last3)]
    avg_cf_ratio = statistics.mean(cf_ratios)
    if avg_cf_ratio > 1.0:
        results['cf_quality'] = 1.0
    elif avg_cf_ratio >= 0.7:
        results['cf_quality'] = 0.5
    else:
        results['cf_quality'] = 0
    results['avg_cf_ratio'] = avg_cf_ratio
    total += results['cf_quality']
    
    # 1.3 资本支出效率（1分）
    capexs = data['capexs']
    fcf_ratios = [(cf - capex) / cf if cf > 0 else 0 for cf, capex in zip(cfs, capexs)]
    avg_fcf_ratio = statistics.mean(fcf_ratios)
    if avg_fcf_ratio > 0.5:
        results['capex_efficiency'] = 1.0
    elif avg_fcf_ratio >= 0.3:
        results['capex_efficiency'] = 0.5
    else:
        results['capex_efficiency'] = 0
    results['avg_fcf_ratio'] = avg_fcf_ratio
    total += results['capex_efficiency']
    
    # ===== 2. 商业模式特征（3分）=====
    
    # 2.1 毛利率水平（1.5分）
    gm = data['gross_margin_latest']
    if gm > 0.4:
        results['gross_margin_score'] = 1.5
    elif gm >= 0.2:
        results['gross_margin_score'] = 0.75
    else:
        results['gross_margin_score'] = 0
    total += results['gross_margin_score']
    
    # 2.2 ROE水平（1.5分）
    roes = data['roes']
    avg_roe = statistics.mean(roes)
    if avg_roe > 0.15:
        results['roe_score'] = 1.5
    elif avg_roe >= 0.08:
        results['roe_score'] = 0.75
    else:
        results['roe_score'] = 0
    results['avg_roe'] = avg_roe
    total += results['roe_score']
    
    # ===== 3. 资本配置与治理（4分）=====
    
    # 3.1 财务保守度（1分）
    dr = data['debt_ratio']
    if dr < 0.4:
        results['financial_conservatism'] = 1.0
    elif dr <= 0.6:
        results['financial_conservatism'] = 0.5
    else:
        results['financial_conservatism'] = 0
    total += results['financial_conservatism']
    
    # 3.2 股东回报力度（1.5分）
    dy = data['dividend_yields']
    avg_dy = statistics.mean(dy)
    dy_trend = dy[-1] >= dy[0]  # 近年是否增长
    if avg_dy > 0.03 and dy_trend:
        results['shareholder_return'] = 1.5
    elif avg_dy >= 0.015:
        results['shareholder_return'] = 0.75
    else:
        results['shareholder_return'] = 0
    results['avg_dividend_yield'] = avg_dy
    total += results['shareholder_return']
    
    # 3.3 资本纪律（1.5分）
    has_bad_ma = data.get('has_high_premium_ma', False)
    has_freq_iss = data.get('has_frequent_issuance', False)
    has_mismatch = data.get('financing_mismatch', False)
    
    if not has_bad_ma and not has_freq_iss and not has_mismatch:
        results['capital_discipline'] = 1.5
    elif sum([has_bad_ma, has_freq_iss, has_mismatch]) == 1:
        results['capital_discipline'] = 0.75
    else:
        results['capital_discipline'] = 0
    total += results['capital_discipline']
    
    results['total_quant_b_score'] = total
    
    # 标记疑点
    results['doubts'] = []
    if results['shareholder_return'] < 1:
        results['doubts'].append('E')  # 管理层漠视股东利益
    if results['capital_discipline'] < 1:
        results['doubts'].append('F')  # 资本纪律问题
    
    return results


def main():
    parser = argparse.ArgumentParser(description='B-Score（量化版）计算脚本（满分10分）')
    
    # 近5年净利润列表（逗号分隔）
    parser.add_argument('--net-incomes', type=str, required=True, help='近5年净利润列表，逗号分隔（如1200,1300,1400,1500,1600），单位：亿元')
    # 近3年经营现金流列表
    parser.add_argument('--operating-cfs', type=str, required=True, help='近3年经营现金流列表，逗号分隔，单位：亿元')
    # 近3年资本支出列表
    parser.add_argument('--capexs', type=str, required=True, help='近3年资本支出列表，逗号分隔，单位：亿元')
    # 毛利率（小数）
    parser.add_argument('--gross-margin-latest', type=float, required=True, help='最新年度毛利率（小数，如0.35表示35%）')
    # 近3年ROE列表
    parser.add_argument('--roes', type=str, required=True, help='近3年ROE列表，逗号分隔（小数，如0.08,0.09,0.10）')
    # 资产负债率
    parser.add_argument('--debt-ratio', type=float, required=True, help='最新年度资产负债率（小数，如0.45表示45%）')
    # 近3年股息率列表
    parser.add_argument('--dividend-yields', type=str, required=True, help='近3年股息率列表，逗号分隔（小数，如0.04,0.045,0.05）')
    # 高溢价并购
    parser.add_argument('--has-high-premium-ma', type=lambda x: x.lower() == 'true', default=False, help='近5年是否有高溢价并购(溢价率>50%) (true/false)')
    # 频繁增发
    parser.add_argument('--has-frequent-issuance', type=lambda x: x.lower() == 'true', default=False, help='近5年是否有频繁增发(>=2次) (true/false)')
    # 融资用途不符
    parser.add_argument('--financing-mismatch', type=lambda x: x.lower() == 'true', default=False, help='融资用途是否与承诺严重不符 (true/false)')
    
    args = parser.parse_args()
    
    data = {
        'net_incomes': [float(x) * 1e8 for x in args.net_incomes.split(',')],
        'operating_cfs': [float(x) * 1e8 for x in args.operating_cfs.split(',')],
        'capexs': [float(x) * 1e8 for x in args.capexs.split(',')],
        'gross_margin_latest': args.gross_margin_latest,
        'roes': [float(x) for x in args.roes.split(',')],
        'debt_ratio': args.debt_ratio,
        'dividend_yields': [float(x) for x in args.dividend_yields.split(',')],
        'has_high_premium_ma': args.has_high_premium_ma,
        'has_frequent_issuance': args.has_frequent_issuance,
        'financing_mismatch': args.financing_mismatch,
    }
    
    result = calc_b_score_quant(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
