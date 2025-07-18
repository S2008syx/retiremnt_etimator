# 运行口令：streamlit run ~/PycharmProjects/PythonProject7/.venv/bin/web1.py
import streamlit as st
import matplotlib.pyplot as plt

# 【一、标题和用户输入】
st.title("退休资产规划模拟器（By Sibo Song）")

years = st.slider("工作期间缴纳401k的年数", 0, 50, 25,
                  help="例如：如果你已经连续缴纳401k共15年，这里填写15。")

user_input = st.number_input("当前401k账户余额（适用于已不再继续缴纳的用户)(若填写，则上方和下方年数和年缴金额不再生效)", value=0,
                             help="如果你还在缴纳401k，可以留空；否则请输入当前余额。")

store = st.number_input("每年缴纳401k金额（退休前）", value=30000,
                        help="如果你每年继续往401k存入资金，请填写此项；否则填0。")

prin = st.number_input("退休时的其他资产总额（不包含401k）", value=5000000,
                       help="例如银行存款、股票、房地产等可流动资产。")

spend = st.number_input("预计每年退休生活开支", value=200000,
                        help="根据生活水平和地区设定支出金额。")

portion = st.slider("每年从401k中提取的资金比例", 0.0, 1.0, 0.5,
                    help="例如：0.5 表示你每年用退休支出的 50% 来自401k，其余来自其他资产。")

interest = st.number_input("预计年化投资收益率（税后）", value=1.06,
                           help="适用于401k与其他资产的综合投资回报率。例如6%请填写1.06。")

inflation = st.number_input("预计年通货膨胀率", value=1.03,
                            help="影响每年支出增长。例如3%通胀请填写1.03。")

# 【二、401k累积阶段】
retire = 0
GroR = interest
for _ in range(years):
    retire = (retire + store) * GroR
if user_input != 0:
    retire = user_input

# 【三、退休模拟】
x = 1
totalP = 0
prin_balance = prin
retire_balance = retire
retire_list = []
totalP_list = []
list_tax = []
Total_spend_list =[]

def get_tax_rate(retire_spend):
    if 0 <= retire_spend <= 11925:
        return 1 - 0.10
    elif 11926 <= retire_spend <= 48475:
        return 1 - ((11925 / retire_spend) * 0.10 + (1 - 11925 / retire_spend) * 0.12)
    elif 48476 <= retire_spend <= 103350:
        return 1 - ((48475 / retire_spend) * 0.108 + (1 - 48475 / retire_spend) * 0.22)
    elif 103351 <= retire_spend <= 197300:
        return 1 - ((103350 / retire_spend) * 0.1708 + (1 - 103350 / retire_spend) * 0.24)
    elif 197301 <= retire_spend <= 250525:
        return 1 - ((197300 / retire_spend) * 0.2037 + (1 - 197300 / retire_spend) * 0.32)
    elif 250526 <= retire_spend <= 626350:
        return 1 - ((250225 / retire_spend) * 0.2248 + (1 - 250225 / retire_spend) * 0.35)
    elif retire_spend > 626350:
        return 1 - ((626350 / retire_spend) * 0.3014 + (1 - 626350 / retire_spend) * 0.37)
    else:
        raise ValueError("retire_spend 不在合理区间")

while x < 51:
    Total_spend = spend * (inflation ** x)
    retire_spend = spend * (inflation ** x) * portion
    tax = get_tax_rate(retire_spend)
    list_tax.append(1-tax)
    Total_spend_list.append(Total_spend)
    prin_balance = prin_balance * interest - spend * (inflation ** x) * (1 - portion)
    retire_balance = retire_balance * interest - retire_spend / tax
    totalP = prin_balance + retire_balance

    retire_list.append(retire_balance)
    totalP_list.append(totalP)

    if retire_balance <= 0:
        totalP -= (1 - list_tax[-1]) * retire_list[-1]
        break
    x += 1

# 【四、401k耗尽后，仅用本金模拟】
while x < 51:
    totalP = totalP * interest - spend * (inflation ** x)
    totalP_list.append(totalP)
    Total_spend_list.append(spend * (inflation ** x))
    if totalP <= 0:
        break
    x += 1

# 【五、图表显示】
fig, ax = plt.subplots()
ax.plot(range(1, len(totalP_list) + 1), totalP_list, label="Total Assets ($)")
ax.set_title("Total Retirement Asset Over Time")
ax.set_xlabel("Years After Retirement")
ax.set_ylabel("Total Assets ($)")
ax.legend()
st.pyplot(fig)
fig, ax = plt.subplots()
ax.plot(range(1, len(list_tax) + 1), list_tax, label="Tax Rates of 401k")
ax.set_title("401k Tax Rate Over the Years")
ax.set_xlabel("Years After Retirement")
ax.set_ylabel("Annually Tax Rates")
ax.legend()
st.pyplot(fig)
fig, ax = plt.subplots()
ax.plot(range(1, len(Total_spend_list) + 1), Total_spend_list, label="Annually Money Spending")
ax.set_title("Annual Spending After Retirement")
ax.set_xlabel("Years After Retirement")
ax.set_ylabel("Annually Spending")
ax.legend()
st.pyplot(fig)

# 【六、附加说明】
st.success("说明：本模拟器假设州税为0。联邦税根据分段税率计算，仅对401k取现部分生效，其他资产不纳入税收考虑。")

