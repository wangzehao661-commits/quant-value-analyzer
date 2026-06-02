#!/usr/bin/env python3
"""
B-Score 完整版（15分制）计算脚本
在量化版（10分）基础上增加4个定性维度（5分）
输入：量化结果 + 定性数据（通过命令行参数）
输出：完整版B-Score评分（JSON格式）
"""

import argparse
import json
import sys


def calc_b_score_full(quant_result: dict, qualitative_data: dict) -> dict:
    """
    计算完整版B-Score（满分15分）
    
    quant_result: 量化版B-Score计算结果
    qualitative_data 字段说明：
    - customer_stickiness: 客户粘性等级 ('very_high' / 'moderate' / 'low')
    - cycle_resilience: 周期穿越能力 ('strong' / 'moderate' / 'average' / 'weak')
    - rd_brand_sustain: 研发/品牌投入持续度 ('increased' / 'slight_decline' / 'significant_cut')
    - mgmt_integrity: 管理层诚信与能力 ('excellent' / 'acceptable' / 'poor')
    """
    
    results = {}
    
    # 继承量化版得分
    results['quant_score'] = quant_result.get('total_quant_b_score', 0)
    results['quant_details'] = quant_result
    
    # ===== 4. 客户粘性与定价权（1.5分）=====
    stickiness_map = {
        'very_high': 1.5,    # 成瘾/社交/刚需+替换成本极高
        'moderate': 0.75,    # 品牌忠诚但竞争充分
        'low': 0,            # 同质化竞争
    }
    results['customer_stickiness_score'] = stickiness_map.get(
        qualitative_data.get('customer_stickiness', 'low'), 0
    )
    results['customer_stickiness_level'] = qualitative_data.get('customer_stickiness', 'low')
    
    # ===== 5. 周期穿越能力（1.5分）=====
    cycle_map = {
        'strong': 1.5,      # 营收降幅 < 行业均值50%
        'moderate': 1.0,    # 优于行业但 < 50%优势
        'average': 0.5,     # 与行业同步
        'weak': 0,          # 更差
    }
    results['cycle_resilience_score'] = cycle_map.get(
        qualitative_data.get('cycle_resilience', 'average'), 0.5
    )
    results['cycle_resilience_level'] = qualitative_data.get('cycle_resilience', 'average')
    results['cycle_evidence'] = qualitative_data.get('cycle_evidence', '')
    
    # ===== 6. 研发/品牌投入持续度（1.5分）=====
    rd_map = {
        'increased': 1.5,           # 利润承压时逆势增加
        'slight_decline': 1.0,      # 微降（<10%）
        'significant_cut': 0,       # 大幅削减（≥10%）
    }
    results['rd_brand_sustain_score'] = rd_map.get(
        qualitative_data.get('rd_brand_sustain', 'slight_decline'), 1.0
    )
    results['rd_brand_sustain_level'] = qualitative_data.get('rd_brand_sustain', 'slight_decline')
    results['rd_brand_evidence'] = qualitative_data.get('rd_brand_evidence', '')
    
    # ===== 7. 管理层诚信与能力（1分）=====
    mgmt_map = {
        'excellent': 1.0,   # 无污点且多次正确决策
        'acceptable': 0.5,  # 基本可信
        'poor': 0,          # 有诚信瑕疵
    }
    results['mgmt_integrity_score'] = mgmt_map.get(
        qualitative_data.get('mgmt_integrity', 'acceptable'), 0.5
    )
    results['mgmt_integrity_level'] = qualitative_data.get('mgmt_integrity', 'acceptable')
    
    # 汇总
    qual_total = (
        results['customer_stickiness_score'] +
        results['cycle_resilience_score'] +
        results['rd_brand_sustain_score'] +
        results['mgmt_integrity_score']
    )
    results['qual_score'] = qual_total
    results['total_full_b_score'] = results['quant_score'] + qual_total
    
    # 星级
    score = results['total_full_b_score']
    if score >= 13:
        results['star_rating'] = 'AAAAA'
        results['rating_desc'] = '卓越'
    elif score >= 10:
        results['star_rating'] = 'AAA'
        results['rating_desc'] = '优秀'
    elif score >= 7:
        results['star_rating'] = 'AA'
        results['rating_desc'] = '中等'
    elif score >= 4:
        results['star_rating'] = 'A'
        results['rating_desc'] = '较弱'
    else:
        results['star_rating'] = 'D'
        results['rating_desc'] = '危险'
    
    # 明细表
    results['scorecard'] = [
        {'dimension': '盈利能力真实性', 'score': results['quant_details'].get('profit_stability', 0) + 
         results['quant_details'].get('cf_quality', 0) + 
         results['quant_details'].get('capex_efficiency', 0), 'max': 3},
        {'dimension': '商业模式特征', 'score': results['quant_details'].get('gross_margin_score', 0) + 
         results['quant_details'].get('roe_score', 0), 'max': 3},
        {'dimension': '资本配置与治理', 'score': results['quant_details'].get('financial_conservatism', 0) + 
         results['quant_details'].get('shareholder_return', 0) + 
         results['quant_details'].get('capital_discipline', 0), 'max': 4},
        {'dimension': '客户粘性与定价权', 'score': results['customer_stickiness_score'], 'max': 1.5},
        {'dimension': '周期穿越能力', 'score': results['cycle_resilience_score'], 'max': 1.5},
        {'dimension': '研发/品牌投入持续度', 'score': results['rd_brand_sustain_score'], 'max': 1.5},
        {'dimension': '管理层诚信与能力', 'score': results['mgmt_integrity_score'], 'max': 1},
    ]
    
    return results


def main():
    parser = argparse.ArgumentParser(description='B-Score 完整版计算脚本（满分15分）')
    
    # 量化得分（从 b_score_quant.py 输出中提取）
    parser.add_argument('--quant-score', type=float, help='量化版B-Score总分（满分10分）')
    parser.add_argument('--quant-json', type=str, help='b_score_quant.py 输出的JSON文件路径；提供后可生成完整量化明细表')
    parser.add_argument('--customer-stickiness', type=str, required=True, choices=['very_high', 'moderate', 'low'], help='客户粘性等级')
    parser.add_argument('--cycle-resilience', type=str, required=True, choices=['strong', 'moderate', 'average', 'weak'], help='周期穿越能力')
    parser.add_argument('--rd-brand-sustain', type=str, required=True, choices=['increased', 'slight_decline', 'significant_cut'], help='研发/品牌投入持续度')
    parser.add_argument('--mgmt-integrity', type=str, required=True, choices=['excellent', 'acceptable', 'poor'], help='管理层诚信与能力')
    parser.add_argument('--cycle-evidence', type=str, default='', help='周期穿越能力的证据描述')
    parser.add_argument('--rd-brand-evidence', type=str, default='', help='研发/品牌投入持续度的证据描述')
    
    args = parser.parse_args()

    if args.quant_json:
        with open(args.quant_json, 'r', encoding='utf-8') as f:
            quant_result = json.load(f)
    elif args.quant_score is not None:
        quant_result = {
            'total_quant_b_score': args.quant_score
        }
    else:
        parser.error('must provide --quant-score or --quant-json')
    
    qualitative_data = {
        'customer_stickiness': args.customer_stickiness,
        'cycle_resilience': args.cycle_resilience,
        'rd_brand_sustain': args.rd_brand_sustain,
        'mgmt_integrity': args.mgmt_integrity,
        'cycle_evidence': args.cycle_evidence,
        'rd_brand_evidence': args.rd_brand_evidence,
    }
    
    result = calc_b_score_full(quant_result, qualitative_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
