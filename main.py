import requests
import json


def request(url, params):
    header = {'XToken': get_XToken()}
    return_json = requests.get(url='https://www.zhixue.com/zhixuebao/report/exam/' + url,
                               params=params, headers=header)
    return_data = json.loads(return_json.content.decode('utf-8'))
    return return_data


def get_XToken():
    global Session
    cookies = dict(tlsysSessionId=Session)
    XToken = requests.get(url="https://www.zhixue.com/addon/error/book/index", cookies=cookies)
    return json.loads(XToken.content.decode('utf-8'))["result"]


def get_exam_list():
    global service_dict, service
    return_data = request(url="getUserExamList", params={})
    exam_dict = return_data["result"]["examList"]
    exam_data = []
    exam_list = {}
    for j in range(len(exam_dict)):  # 提取信息
        now_exam = return_data["result"]["examList"][j]
        exam_data += [{"time": now_exam["examCreateDateTime"],
                       "id": now_exam["examId"],
                       "name": now_exam["examName"],
                       "type": now_exam["examType"]}]  # 可拓展获取其他信息
        exam_list[now_exam["examName"]] = now_exam["examId"]
    global param_data
    param_data = exam_list
    return exam_data


def bank(data):
    data = data["result"]["list"]
    bank_dict = {}
    for p in range(len(data)):
        bank_dict[data[p]["subjectName"]] = data[p]["rationalRank"]
    return bank_dict


def scores(data):
    data = data["result"]["paperList"]
    scores_dict = {}
    for q in range(len(data)):
        scores_dict[data[q]["subjectName"]] = str(data[q]["userScore"]) + "/" + str(int(data[q]["standardScore"]))
    return scores_dict


def print_exam_list():
    i_int = 0
    for i in list(param_data.keys()):
        i_int += 1
        print(str(i_int) + "." + str(i))


service_dict = {"分数": "getReportMain",
                "排名": "getSubjectDiagnosis",
                "考试列表": "getUserExamList"}
service = ""
param_data = {}

help_info = """请输入session!（session重新登陆后会过期）
方法:
1.打开浏览器，登陆智学网。
2.找到左上角的网址左边的“锁”的图标（刷新按钮右边），点击。
3.在弹出的页面中点击“Cookie（正在使用xx个Cookie）”。
4.在弹出的“正在使用Cookie”中点击“www.zhixue.com”。
5.再次点击列表中的“Cookie”。
6.翻到现在列表中有的最后一个像调色盘一样的图标，叫“tlsysSessionId”（非常后面），点击。
7.在下面显示的详细信息中复制它的内容，看起来像“xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx”。
8.粘贴进窗口"""


def main():
    global service, param_data
    service = input("选择服务(分数/排名/考试列表):")

    param_data = {}
    get_exam_list()  # 获取考试列表

    if service == "考试列表":
        print_exam_list()
    else:
        print("\n", end="")
        print_exam_list()

        number = input("选择报告(输入数字):")
        print("\n", end="")

        response = request(url=service_dict[service],
                           params={"examId": param_data[list(param_data.keys())[int(number) - 1]]})

        if service == "排名":
            print("每科排名:", bank(response))
            print("p.s.每科排名的数字代表您的成绩在100人中的大致排名。")
        elif service == "分数":
            print("每科分数:", scores(response))

    print("")


if __name__ == "__main__":
    Session = ""
    while Session == "":
        print(help_info)
        Session = input("Session:")

    while True:
        try:
            main()
        except Exception as exp:
            print("出错，请按提示输入或重启程序。出错信息:\n", exp)
