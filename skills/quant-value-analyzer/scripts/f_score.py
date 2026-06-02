#!/usr/bin/env python3
"""
F-Score 计算脚本
输入：财务数据字典（通过命令行参数）
输出：F-Score 各项得分及总分（JSON格式）
"""

import argparse
import json
import sys


def calc_f_score(data: dict) -> dict:
    """
    计算Piotroski F-Score
    
    data 字段说明：
    - net_income: 最新年度归母净利润
    - operating_cf: 最新年度经营活动现金流净额
    - net_income_prev: 上年度归母净利润
    - operating_cf_prev: 上年度经营活动现金流净额
    - total_assets: 最新年度总资产
    - total_assets_prev: 上年度总资产
    - long_term_debt: 最新年度非流动负债合计
    - long_term_debt_prev: 上年度非流动负债合计
    - current_assets: 最新年度流动资产
    - current_liabilities: 最新年度流动负债
    - current_assets_prev: 上年度流动资产
    - current_liabilities_prev: 上年度流动负债
    - has_equity_issuance: 近一年是否有增发 (bool)
    - gross_profit: 最新年度毛利润
    - revenue: 最新年度营业收入
    - gross_profit_prev: 上年度毛利润
    - revenue_prev: 上年度营业收入
    """
    
    results = {}
    total = 0
    
    # ① 净利润 > 0
    results['s1_net_income_positive'] = 1 if data['net_income'] > 0 else 0
    total += results['s1_net_income_positive']
    
    # ② 经营现金流 > 0
    results['s2_operating_cf_positive'] = 1 if data['operating_cf'] > 0 else 0
    total += results['s2_operating_cf_positive']
    
    # ③ 经营现金流 > 净利润
    results['s3_cf_gt_income'] = 1 if data['operating_cf'] > data['net_income'] else 0
    total += results['s3_cf_gt_income']
    
    # ④ ROA同比提高
    roa_current = data['net_income'] / data['total_assets']
    roa_prev = data['net_income_prev'] / data['total_assets_prev']
    results['s4_roa_improved'] = 1 if roa_current > roa_prev else 0
    total += results['s4_roa_improved']
    results['roa_current'] = roa_current
    results['roa_prev'] = roa_prev
    
    # ⑤ 长期负债率同比下降
    lt_debt_ratio_current = data['long_term_debt'] / data['total_assets']
    lt_debt_ratio_prev = data['long_term_debt_prev'] / data['total_assets_prev']
    results['s5_lt_debt_ratio_improved'] = 1 if lt_debt_ratio_current < lt_debt_ratio_prev else 0
    total += results['s5_lt_debt_ratio_improved']
    results['lt_debt_ratio_current'] = lt_debt_ratio_current
    results['lt_debt_ratio_prev'] = lt_debt_ratio_prev
    
    # ⑥ 流动比率同比提高
    current_ratio = data['current_assets'] / data['current_liabilities']
    current_ratio_prev = data['current_assets_prev'] / data['current_liabilities_prev']
    results['s6_current_ratio_improved'] = 1 if current_ratio > current_ratio_prev else 0
    total += results['s6_current_ratio_improved']
    results['current_ratio'] = current_ratio
    results['current_ratio_prev'] = current_ratio_prev
    
    # ⑦ 近一年未增发
    results['s7_no_equity_issuance'] = 0 if data['has_equity_issuance'] else 1
    total += results['s7_no_equity_issuance']
    
    # ⑧ 毛利率同比提高
    gross_margin_current = data['gross_profit'] / data['revenue']
    gross_margin_prev = data['gross_profit_prev'] / data['revenue_prev']
    results['s8_gross_margin_improved'] = 1 if gross_margin_current > gross_margin_prev else 0
    total += results['s8_gross_margin_improved']
    results['gross_margin_current'] = gross_margin_current
    results['gross_margin_prev'] = gross_margin_prev
    
    # ⑨ 资产周转率同比提高
    asset_turnover_current = data['revenue'] / data['total_assets']
    asset_turnover_prev = data['revenue_prev'] / data['total_assets_prev']
    results['s9_asset_turnover_improved'] = 1 if asset_turnover_current > asset_turnover_prev else 0
    total += results['s9_asset_turnover_improved']
    results['asset_turnover_current'] = asset_turnover_current
    results['asset_turnover_prev'] = asset_turnover_prev
    
    results['total_f_score'] = total
    
    # 标记疑点
    results['doubts'] = []
    if results['s3_cf_gt_income'] == 0:
        results['doubts'].append('B')  # 利润含金量存疑
    if results['s8_gross_margin_improved'] == 0:
        results['doubts'].append('C')  # 毛利率下滑
    if results['s9_asset_turnover_improved'] == 0:
        results['doubts'].append('D')  # 资产效率下降
    
    return results


def main():
    parser = argparse.ArgumentParser(description='F-Score 计算脚本（9分制财务防雷扫描）')
    parser.add_argument('--net-income', type=float, required=True, help='最新年度归母净利润（元）')
    parser.add_argument('--operating-cf', type=float, required=True, help='最新年度经营活动现金流净额（元）')
    parser.add_argument('--net-income-prev', type=float, required=True, help='上年度归母净利润（元）')
    parser.add_argument('--operating-cf-prev', type=float, required=True, help='上年度经营活动现金流净额（元）')
    parser.add_argument('--total-assets', type=float, required=True, help='最新年度总资产（元）')
    parser.add_argument('--total-assets-prev', type=float, required=True, help='上年度总资产（元）')
    parser.add_argument('--long-term-debt', type=float, required=True, help='最新年度非流动负债合计（元）')
    parser.add_argument('--long-term-debt-prev', type=float, required=True, help='上年度非流动负债合计（元）')
    parser.add_argument('--current-assets', type=float, required=True, help='最新年度流动资产（元）')
    parser.add_argument('--current-liabilities', type=float, required=True, help='最新年度流动负债（元）')
    parser.add_argument('--current-assets-prev', type=float, required=True, help='上年度流动资产（元）')
    parser.add_argument('--current-liabilities-prev', type=float, required=True, help='上年度流动负债（元）')
    parser.add_argument('--has-equity-issuance', type=lambda x: x.lower() == 'true', default=False, help='近一年是否有增发 (true/false)')
    parser.add_argument('--gross-profit', type=float, required=True, help='最新年度毛利润（元）')
    parser.add_argument('--revenue', type=float, required=True, help='最新年度营业收入（元）')
    parser.add_argument('--gross-profit-prev', type=float, required=True, help='上年度毛利润（元）')
    parser.add_argument('--revenue-prev', type=float, required=True, help='上年度营业收入（元）')
    
    args = parser.parse_args()
    
    data = {
        'net_income': args.net_income,
        'operating_cf': args.operating_cf,
        'net_income_prev': args.net_income_prev,
        'operating_cf_prev': args.operating_cf_prev,
        'total_assets': args.total_assets,
        'total_assets_prev': args.total_assets_prev,
        'long_term_debt': args.long_term_debt,
        'long_term_debt_prev': args.long_term_debt_prev,
        'current_assets': args.current_assets,
        'current_liabilities': args.current_liabilities,
        'current_assets_prev': args.current_assets_prev,
        'current_liabilities_prev': args.current_liabilities_prev,
        'has_equity_issuance': args.has_equity_issuance,
        'gross_profit': args.gross_profit,
        'revenue': args.revenue,
        'gross_profit_prev': args.gross_profit_prev,
        'revenue_prev': args.revenue_prev,
    }
    
    result = calc_f_score(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
