"""
测试运行脚本
提供多种测试运行方式
"""
import sys
import os
import subprocess
from datetime import datetime


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("运行所有测试用例")
    print("=" * 60)
    cmd = ["pytest", "tests", "-v"]  # 改这里：去掉斜杠
    subprocess.run(cmd)


def run_dao_tests():
    """只运行DAO测试"""
    print("=" * 60)
    print("运行DAO测试用例")
    print("=" * 60)
    cmd = ["pytest", "tests", "-v", "-k", "dao"]  # 改这里
    subprocess.run(cmd)


def run_query_tests():
    """只运行SQL查询测试"""
    print("=" * 60)
    print("运行SQL查询测试用例")
    print("=" * 60)
    cmd = ["pytest", os.path.join("tests", "test_sql_queries.py"), "-v", "-m", "query"]  # 改这里
    subprocess.run(cmd)


def run_procedure_tests():
    """只运行存储过程测试"""
    print("=" * 60)
    print("运行存储过程测试用例")
    print("=" * 60)
    cmd = ["pytest", "tests", "-v", "-m", "procedure"]  # 改这里
    subprocess.run(cmd)


def run_specific_test(test_file):
    """运行指定测试文件"""
    print("=" * 60)
    print(f"运行测试文件: {test_file}")
    print("=" * 60)
    cmd = ["pytest", os.path.join("tests", test_file), "-v"]  # 改这里
    subprocess.run(cmd)


def generate_html_report():
    """生成HTML测试报告"""
    print("=" * 60)
    print("生成HTML测试报告")
    print("=" * 60)
    
    # 创建报告目录
    os.makedirs("reports", exist_ok=True)
    
    # 生成报告文件名（带时间戳）
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join("reports", f"test_report_{timestamp}.html")  # 改这里
    
    cmd = [
        "pytest", 
        "tests",  # 改这里
        "-v",
        f"--html={report_file}",
        "--self-contained-html"
    ]
    subprocess.run(cmd)
    
    print(f"\n测试报告已生成: {report_file}")


def run_with_coverage():
    """运行测试并生成覆盖率报告"""
    print("=" * 60)
    print("运行测试并生成覆盖率报告")
    print("=" * 60)
    
    cmd = [
        "pytest",
        "tests",  # 改这里
        "-v",
        "--cov=dao",
        "--cov-report=html",
        "--cov-report=term"
    ]
    subprocess.run(cmd)
    
    print("\n覆盖率报告已生成: htmlcov/index.html")


def main():
    """主函数"""
    print("\n国家公园智慧管理系统 - 测试运行器")
    print("=" * 60)
    print("请选择测试类型：")
    print("1. 运行所有测试")
    print("2. 只运行DAO测试")
    print("3. 只运行SQL查询测试")
    print("4. 只运行存储过程测试")
    print("5. 生成HTML测试报告")
    print("6. 运行测试并生成覆盖率报告")
    print("7. 运行指定测试文件")
    print("0. 退出")
    print("=" * 60)
    
    choice = input("请输入选项（0-7）: ").strip()
    
    if choice == "1":
        run_all_tests()
    elif choice == "2":
        run_dao_tests()
    elif choice == "3":
        run_query_tests()
    elif choice == "4":
        run_procedure_tests()
    elif choice == "5":
        generate_html_report()
    elif choice == "6":
        run_with_coverage()
    elif choice == "7":
        print("\n可用的测试文件:")
        print("  - test_monitoring_dao.py")
        print("  - test_environment_dao.py")
        print("  - test_visitor_dao.py")
        print("  - test_enforcement_dao.py")
        print("  - test_research_dao.py")
        print("  - test_sql_queries.py")
        test_file = input("\n请输入测试文件名: ").strip()
        run_specific_test(test_file)
    elif choice == "0":
        print("退出测试运行器")
        sys.exit(0)
    else:
        print("无效的选项！")
        sys.exit(1)


if __name__ == "__main__":
    main()