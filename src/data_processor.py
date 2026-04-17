"""
データ前処理・指標抽出モジュール
"""
import zipfile
import io
from bs4 import BeautifulSoup


def extract_diversity_metrics(zip_content: bytes, company_name: str) -> dict:
    """
    ZIPファイルから女性活躍指標を抽出する
    - 女性管理職比率
    - 男性育児休業取得率
    - 男女賃金格差
    """
    zip_file = zipfile.ZipFile(io.BytesIO(zip_content))
    file_list = zip_file.namelist()
    honbun_files = [f for f in file_list if 'honbun' in f and f.endswith('.htm')]

    metrics = {
        'company_name': company_name,
        'female_manager_ratio': None,
        'male_childcare_leave_rate': None,
        'gender_wage_gap': None
    }

    tag_map = {
        'female_manager_ratio': 'jpcrp_cor:RatioOfFemaleEmployeesInManagerialPositionsMetricsOfReportingCompany',
        'male_childcare_leave_rate': 'jpcrp_cor:AllEmployeesCalculatedBasedOnProvisionsOfArticle714Item1OfOrdinanceForEnforcementOfActOnChildcareLeaveCaregiverLeaveAndOtherMeasuresForTheWelfareOfWorkersCaringForChildrenOrOtherFamilyMembersRatioOfMaleEmployeesTakingChildcareLeaveMetricsOfReportingCompany',
        'gender_wage_gap': 'jpcrp_cor:AllEmployeesDifferencesInWagesBetweenMaleAndFemaleEmployeesMetricsOfReportingCompany'
    }

    for honbun_file in honbun_files:
        with zip_file.open(honbun_file) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            for metric, tag_name in tag_map.items():
                if metrics[metric] is not None:
                    continue
                tag = soup.find(attrs={'name': tag_name})
                if tag and tag.get_text(strip=True):
                    try:
                        metrics[metric] = float(tag.get_text(strip=True).replace(',', ''))
                    except:
                        pass

    return metrics


def extract_financial_data(zip_content: bytes, company_name: str) -> dict:
    """
    ZIPファイルから財務データを抽出する
    - 売上高
    - 純利益
    """
    zip_file = zipfile.ZipFile(io.BytesIO(zip_content))
    file_list = zip_file.namelist()
    honbun_files = [f for f in file_list if 'honbun' in f and f.endswith('.htm')]

    financials = {
        'company_name': company_name,
        'net_sales': None,
        'net_profit': None
    }

    tag_map = {
        'net_sales': 'jpcrp_cor:NetSalesSummaryOfBusinessResults',
        'net_profit': 'jpcrp_cor:ProfitLossAttributableToOwnersOfParentSummaryOfBusinessResults'
    }

    for honbun_file in honbun_files:
        with zip_file.open(honbun_file) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            for metric, tag_name in tag_map.items():
                if financials[metric] is not None:
                    continue
                tags = soup.find_all(attrs={'name': tag_name})
                if tags:
                    for tag in tags:
                        text = tag.get_text(strip=True).replace(',', '')
                        try:
                            financials[metric] = float(text)
                            break
                        except:
                            pass

    return financials