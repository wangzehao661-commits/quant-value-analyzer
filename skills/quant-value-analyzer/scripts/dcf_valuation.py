#!/usr/bin/env python3
"""
两阶段DCF估值计算脚本
输入：估值参数（通过命令行参数）
输出：每股内在价值及安全边际（JSON格式）
"""

import argparse
import json
import sys


def two_stage_dcf(
    base_fcf: float,        # 基准自由现金流（亿元）
    g1: float,              # 阶段一增长率（小数，如0.08）
    n_years: int,           # 阶段一年数（通常3-5年）
    g2: float,              # 永续增长率（小数，如0.025）
    wacc: float,            # 折现率（小数，如0.10）
    net_debt: float,        # 净债务（亿元）= 有息负债 - 现金
    total_shares: float,    # 总股本（亿股）
    current_price: float,   # 当前股价（元）
) -> dict:
    """
    两阶段DCF估值
    返回详细的计算过程和结果
    """
    if n_years <= 0:
        raise ValueError('n_years must be greater than 0')
    if wacc <= g2:
        raise ValueError('wacc must be greater than g2 for terminal value calculation')
    if total_shares <= 0:
        raise ValueError('total_shares must be greater than 0')
    
    results = {}
    
    # 阶段一：逐年预测和折现
    stage1_pv = 0
    yearly_details = []
    fcf = base_fcf
    
    for year in range(1, n_years + 1):
        fcf = fcf * (1 + g1)
        discount_factor = 1 / (1 + wacc) ** year
        pv = fcf * discount_factor
        stage1_pv += pv
        yearly_details.append({
            'year': year,
            'fcf': round(fcf, 2),
            'discount_factor': round(discount_factor, 6),
            'present_value': round(pv, 2)
        })
    
    results['stage1_details'] = yearly_details
    results['stage1_total_pv'] = round(stage1_pv, 2)
    
    # 阶段二：终值
    terminal_fcf = fcf * (1 + g2)
    terminal_value = terminal_fcf / (wacc - g2)
    terminal_pv = terminal_value / (1 + wacc) ** n_years
    
    results['terminal_fcf'] = round(terminal_fcf, 2)
    results['terminal_value'] = round(terminal_value, 2)
    results['terminal_pv'] = round(terminal_pv, 2)
    
    # 企业价值
    ev = stage1_pv + terminal_pv
    results['enterprise_value'] = round(ev, 2)
    
    # 股权价值
    equity_value = ev - net_debt
    results['equity_value'] = round(equity_value, 2)
    
    # 每股内在价值
    intrinsic_value_per_share = equity_value / total_shares
    results['intrinsic_value_per_share'] = round(intrinsic_value_per_share, 2)
    
    # 安全边际
    safety_margin = (intrinsic_value_per_share - current_price) / intrinsic_value_per_share * 100
    results['safety_margin'] = round(safety_margin, 2)
    results['current_price'] = current_price
    
    # 判断
    if safety_margin > 30:
        results['valuation_verdict'] = '显著低估'
    elif safety_margin > 15:
        results['valuation_verdict'] = '适度低估'
    elif safety_margin > 0:
        results['valuation_verdict'] = '轻微低估'
    elif safety_margin > -15:
        results['valuation_verdict'] = '合理偏高'
    else:
        results['valuation_verdict'] = '显著高估'

    results['sensitivity_matrix'] = build_sensitivity_matrix(
        base_fcf=base_fcf,
        g1=g1,
        n_years=n_years,
        g2=g2,
        wacc=wacc,
        net_debt=net_debt,
        total_shares=total_shares,
    )
    
    return results


def _intrinsic_value_only(
    base_fcf: float,
    g1: float,
    n_years: int,
    g2: float,
    wacc: float,
    net_debt: float,
    total_shares: float,
) -> float:
    if wacc <= g2:
        return None

    stage1_pv = 0
    fcf = base_fcf
    for year in range(1, n_years + 1):
        fcf *= 1 + g1
        stage1_pv += fcf / (1 + wacc) ** year

    terminal_fcf = fcf * (1 + g2)
    terminal_value = terminal_fcf / (wacc - g2)
    terminal_pv = terminal_value / (1 + wacc) ** n_years
    equity_value = stage1_pv + terminal_pv - net_debt
    return round(equity_value / total_shares, 2)


def build_sensitivity_matrix(
    base_fcf: float,
    g1: float,
    n_years: int,
    g2: float,
    wacc: float,
    net_debt: float,
    total_shares: float,
) -> list:
    rows = []
    for growth in [g1 - 0.02, g1, g1 + 0.02]:
        row = {'g1': round(growth, 4)}
        for discount in [wacc - 0.01, wacc, wacc + 0.01]:
            key = f"wacc_{round(discount, 4)}"
            row[key] = _intrinsic_value_only(
                base_fcf=base_fcf,
                g1=growth,
                n_years=n_years,
                g2=g2,
                wacc=discount,
                net_debt=net_debt,
                total_shares=total_shares,
            )
        rows.append(row)
    return rows


def main():
    parser = argparse.ArgumentParser(description='两阶段DCF估值计算脚本')
    
    parser.add_argument('--base-fcf', type=float, required=True, help='基准自由现金流（亿元）')
    parser.add_argument('--g1', type=float, required=True, help='阶段一增长率（小数，如0.08表示8%）')
    parser.add_argument('--n-years', type=int, required=True, help='阶段一年数（通常3-5年）')
    parser.add_argument('--g2', type=float, required=True, help='永续增长率（小数，如0.025表示2.5%）')
    parser.add_argument('--wacc', type=float, required=True, help='折现率（小数，如0.10表示10%）')
    parser.add_argument('--net-debt', type=float, required=True, help='净债务（亿元）= 有息负债 - 现金')
    parser.add_argument('--total-shares', type=float, required=True, help='总股本（亿股）')
    parser.add_argument('--current-price', type=float, required=True, help='当前股价（元）')
    
    args = parser.parse_args()
    
    result = two_stage_dcf(
        base_fcf=args.base_fcf,
        g1=args.g1,
        n_years=args.n_years,
        g2=args.g2,
        wacc=args.wacc,
        net_debt=args.net_debt,
        total_shares=args.total_shares,
        current_price=args.current_price,
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
