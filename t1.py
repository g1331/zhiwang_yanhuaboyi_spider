import http.client
import re
from bs4 import BeautifulSoup


class YanHuaBoYi(object):
    def __init__(self, page, index, article_type):
        """
        初始化
        :param page: 页数
        :param index: 第几篇文章
        :param article_type: 1是学术期刊,2是学位论文
        """
        self.index = index - 1
        if self.index < 0:
            print('文章序号必须大于等于1')
            exit()
        self.page = str(page)
        self.type = article_type
        self.url = self.get_page_url()
        self.html = self.get_page_info()

    def get_page_url(self):
        """
        获取第一页的知网文章
        :return: 文章直链
        """
        index = self.index
        page = self.page
        type_dict = {
            1: 'CFLQ',
            2: 'CDMD'
        }
        if self.type not in type_dict:
            print('文章类型:1是学术期刊,2是学位论文')
            exit()
        conn = http.client.HTTPSConnection("kns.cnki.net")
        if page == 1:
            IsSearch = 'true'
        else:
            IsSearch = 'false'
        if self.page == 1:
            payload = f"IsSearch={IsSearch}" \
                      f"&QueryJson=%7B%22Platform%22%3A%22%22%2C%22DBCode%22%3A%22" \
                      f"{type_dict[self.type]}%22%2C%22" \
                      f"KuaKuCode%22%3A%22%22%2C%22" \
                      f"QNode%22%3A%7B%22" \
                      f"QGroup%22%3A%5B%7B%22" \
                      f"Key%22%3A%22" \
                      f"Subject%22%2C%22" \
                      f"Title%22%3A%22%22%2C%22" \
                      f"Logic%22%3A1%2C%22" \
                      f"Items%22%3A%5B%7B%22" \
                      f"Title%22%3A%22%E4%B8%BB%E9%A2%98%22%2C%22" \
                      f"Name%22%3A%22SU%22%2C%22" \
                      f"Value%22%3A%22%E6%BC%94%E5%8C%96%E5%8D%9A%E5%BC%88%22%2C%22" \
                      f"Operate%22%3A%22%25%3D%22%2C%22" \
                      f"BlurType%22%3A%22%22%7D%5D%2C%22" \
                      f"ChildItems%22%3A%5B%5D%7D%5D%7D%7D" \
                      f"&SearchSql=2827E4B6502D8710F4C63FA68A0E7A152D8972E3EF5541A46DDE8B3A62A549C1B093F0A10875FEBDE5B17F4F918A6F10CAA2EA622595552DEE59C9627930D8AA16C4AEE03761E9763755CFB4AB484B0A8B7EF2B8C90286C2DEC78CD0E3AE2DB9B3BE203F0BDCAD4BCDFF877136D437E9DCE523BB91848194E9042A1EF42639481893C32BC15EB49F8DBA6D88E0BE298A81A2A10E0803C3F010CB7FA11AA1A188E6726B6A7F4FD1C636081BE13C709F99462180D1BA1B79C9098ADE36A48F3CCE2B1B78B0A17F7A5C77FADBBE119FDF3E7C8AFB383F33B5F6EB3B6B6C6D79B830FD7B151288283EE5D974D96297962072C0D40233CCAFEE9C6498694742FE2D80FCAAA0FABC4D63452A8EC9796C58C80333763B655C7C0320539DF1A90468E26D37D70D269AAAAFF3E3B04C1DC5D26B485836840CD0CB5372BB7336EEC13900D63CE4340AFB729888F8A144ABD212A6B34FAAFA6D1E5439D516FFED876EB0F8D68C613D561024DD68F2009006DB8FA215E521048042041D8E8A3E69F019137BBC029BC474CA02BDA146F1C234D135725FF5EA178CDA3AB8304742D417E95D79A47D1C1378F6B9586ED9ED0B1A886633E6C5630DEB57C5B253290AD78041CE70B4847BFA299012FF1020413DF186908A51BD59D66C9AF8AC95C68D9EFAAF3F7C0268D662FA2BB9F17B0D6E8A9488F27C79CDF23D4DC15A1F5A2E7AC8B86FDE619C10C36805FBCF1917510D091DBF76C7B90D92A761A28EE3050C5AB5D2B5675CF86D03EB70EB6CC3E8FFB685A4390394C71475B56BF1E3AD45BBC2AC45221795D0A9FF733A6A5E31D73407BD10E50267DE6655D6B04D1980ED447E96806489766D94950E346F296415EA9CD72F1D9A4DDC1690D3A5B43DCD14B732E89F3F04E48378BEF7C8B7397C57B7873B4232AC29E77A5E6790397DEBE1C498C1980F9F13F26E4FC31951A5A6ED9FE2EE80608F09A778F806CC129FE113B4CFCB500FF324C2B13617573945F8D9AA92C544E03CC2B9234726757135F53D7EBB12F4E4BC5C6D7702793B23E37598B7070F2267CB166547FE45E445A881134FE00D9D3E3D5C041F973D6FE3D83635BB70B21E0F6D804F47A772FCEE5A8C9298497BFC8EDF97B1707A975F8E148740DF3F7648E92E132D5BA61EF1AB103305C3E3E008DF2E9398D0D47047570CEE576EA09B0AEAE55B15F6456221327031D6880BDBA6432A488A801D65350DB5C40D0E087753851488F646EA3AC2C82300495D93BB13AE3D72235FC788FC2C681200C065F0FB310F9BF781764774C6CF8B929A6BA9B38DBAC5583E655604E0B5B7078C5D49CA29F046A545A43B1125E416DC2050C8B37FCD556384F0402E6F5D36F8AA848F5E15CD5D1DB96C5EBEEC51D9DE77242A69C1F6A7CC2D754AE7A609647FE0BE5E2DA5411F8F924CC29B0A04F6CA32396887EA3A3B633B96D3215B3E9E8C" \
                      f"&PageName=defaultresult" \
                      f"&HandlerId=36" \
                      f"&DBCode={type_dict[self.type]}" \
                      f"&KuaKuCodes=" \
                      f"&CurPage={page}" \
                      f"&RecordsCntPerPage=50" \
                      f"&CurDisplayMode=listmode" \
                      f"&CurrSortField=" \
                      f"&CurrSortFieldType=desc" \
                      f"&IsSortSearch=false" \
                      f"&IsSentenceSearch=false" \
                      f"&Subject="
        else:
            payload = f"IsSearch={IsSearch}" \
                      f"&QueryJson=%7B%22" \
                      f"Platform%22%3A%22%22%2C%22" \
                      f"DBCode%22%3A%22" \
                      f"{type_dict[self.type]}" \
                      f"%22%2C%22" \
                      f"KuaKuCode%22%3A%22%22%2C%22" \
                      f"QNode%22%3A%7B%22" \
                      f"QGroup%22%3A%5B%7B%22" \
                      f"Key%22%3A%22" \
                      f"Subject%22%2C%22" \
                      f"Title%22%3A%22%22%2C%22" \
                      f"Logic%22%3A1%2C%22" \
                      f"Items%22%3A%5B%7B%22" \
                      f"Title%22%3A%22%E4%B8%BB%E9%A2%98%22%2C%2" \
                      f"2Name%22%3A%22SU%22%2C%22" \
                      f"Value%22%3A%22%E6%BC%94%E5%8C%96%E5%8D%9A%E5%BC%88%22%2C%22O" \
                      f"perate%22%3A%22%25%3D%22%2C%22" \
                      f"BlurType%22%3A%22%22%7D%5D%2C%22" \
                      f"ChildItems%22%3A%5B%5D%7D%5D%7D%7D&" \
                      f"SearchSql=2827E4B6502D8710F4C63FA68A0E7A152D8972E3EF5541A46DDE8B3A62A549C1B093F0A10875FEBDE5B17F4F918A6F10CAA2EA622595552DEE59C9627930D8AA16C4AEE03761E9763755CFB4AB484B0A8B7EF2B8C90286C2DEC78CD0E3AE2DB9B3BE203F0BDCAD4BCDFF877136D437E9DCE523BB91848194E9042A1EF42639481893C32BC15EB49F8DBA6D88E0BE298A81A2A10E0803C3F010CB7FA11AA1A188E6726B6A7F4FD1C636081BE13C709F99462180D1BA1B79C9098ADE36A48F3CCE2B1B78B0A17F7A5C77FADBBE119FDF3E7C8AFB383F33B5F6EB3B6B6C6D79B830FD7B151288283EE5D974D96297962072C0D40233CCAFEE9C6498694742FE2D80FCAAA0FABC4D63452A8EC9796C58C80333763B655C7C0320539DF1A90468E26D37D70D269AAAAFF3E3B04C1DC5D26B485836840CD0CB5372BB7336EEC13900D63CE4340AFB729888F8A144ABD212A6B34FAAFA6D1E5439D516FFED876EB0F8D68C613D561024DD68F2009006DB8FA215E521048042041D8E8A3E69F019137BBC029BC474CA02BDA146F1C234D135725FF5EA178CDA3AB8304742D417E95D79A47D1C1378F6B9586ED9ED0B1A886633E6C5630DEB57C5B253290AD78041CE70B4847BFA299012FF1020413DF186908A51BD59D66C9AF8AC95C68D9EFAAF3F7C0268D662FA2BB9F17B0D6E8A9488F27C79CDF23D4DC15A1F5A2E7AC8B86FDE619C10C36805FBCF1917510D091DBF76C7B90D92A761A28EE3050C5AB5D2B5675CF86D03EB70EB6CC3E8FFB685A4390394C71475B56BF1E3AD45BBC2AC45221795D0A9FF733A6A5E31D73407BD10E50267DE6655D6B04D1980ED447E96806489766D94950E346F296415EA9CD72F1D9A4DDC1690D3A5B43DCD14B732E89F3F04E48378BEF7C8B7397C57B7873B4232AC29E77A5E6790397DEBE1C498C1980F9F13F26E4FC31951A5A6ED9FE2EE80608F09A778F806CC129FE113B4CFCB500FF324C2B13617573945F8D9AA92C544E03CC2B9234726757135F53D7EBB12F4E4BC5C6D7702793B23E37598B7070F2267CB166547FE45E445A881134FE00D9D3E3D5C041F973D6FE3D83635BB70B21E0F6D804F47A772FCEE5A8C9298497BFC8EDF97B1707A975F8E148740DF3F7648E92E132D5BA61EF1AB103305C3E3E008DF2E9398D0D47047570CEE576EA09B0AEAE55B15F6456221327031D6880BDBA6432A488A801D65350DB5C40D0E087753851488F646EA3AC2C82300495D93BB13AE3D72235FC788FC2C681200C065F0FB310F9BF781764774C6CF8B929A6BA9B38DBAC5583E655604E0B5B7078C5D49CA29F046A545A43B1125E416DC2050C8B37FCD556384F0402E6F5D36F8AA848F5E15CD5D1DB96C5EBEEC51D9DE77242A69C1F6A7CC2D754AE7A609647FE0BE5E2DA5411F8F924CC29B0A04F6CA32396887EA3A3B633B96D3215B3E9E8C&" \
                      f"PageName=defaultresult&HandlerId=40" \
                      f"&DBCode={type_dict[self.type]}" \
                      f"&KuaKuCodes=" \
                      f"&CurPage={page}" \
                      f"&RecordsCntPerPage=20" \
                      f"&CurDisplayMode=listmode" \
                      f"&CurrSortField=" \
                      f"&CurrSortFieldType=desc" \
                      f"&IsSortSearch=false" \
                      f"&IsSentenceSearch=false" \
                      f"&Subject="

        headers = {
            'Host': ' kns.cnki.net',
            'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
            'Accept': ' text/html, */*; q=0.01',
            'Accept-Language': ' zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer': ' https://kns.cnki.net/kns8/defaultresult/index',
            'X-Requested-With': ' XMLHttpRequest',
            'Origin': ' https://kns.cnki.net',
            'Connection': ' keep-alive',
            'Cookie': ' Ecp_notFirstLogin=SkaNuh; '
                      'cangjieStatus_NZKPT2=true; '
                      'cangjieConfig_NZKPT2=%7B%22status%22%3Atrue%2C%22startTime%22%3A%222022-10-20%22%2C%22endTime'
                      '%22%3A%222023-10-20%22%2C%22orginHosts%22%3A%22kns.cnki.net%22%2C%22type%22%3A%'
                      '22mix%22%2C%22poolSize%22%3A%2210%22%2C%22intervalTime%22%3A10000%2C%22persist%'
                      '22%3Afalse%7D; SID_sug=126003; ASP.NET_SessionId=p5m4o3xrlg11vbb2dzxod5y0; '
                      'SID_kns8=123154; dblang=ch; CurrSortField=%e7%9b%b8%e5%85%b3%e5%ba%a6%2frelevant%'
                      '2c(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27time%27)+desc; CurrSortFieldType=desc; '
                      'SID_kns_new=kns25128004; SID_docpre=128007; SID_kcms=025126024; '
                      '_pk_id=0a637184-eb1d-4c77-9a8c-d13f788f4b70.1666772312.1.1666773138.1666772312.; '
                      '_pk_ref=%5B%22%22%2C%22%22%2C1666772312%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl'
                      '%3DRkL9J16nXRcfF_omFFvMbIh74gXh2W7oE44uvnJrPFW%26wd%3D%26eqid'
                      '%3Da67f19810002aad8000000036358ed4e%22%5D; Ecp_ClientId=a221026161802477663; '
                      'Ecp_LoginStuts={"IsAutoLogin":false,"UserName":"XN0047","ShowName":"%E5%9B%9B'
                      '%E5%B7%9D%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6","UserType":"bk","BUserName":"",'
                      '"BShowName":"","BUserType":"","r":"SkaNuh","Members":[]}; '
                      'c_m_LinID=LinID=WEEvREcwSlJHSldSdmVpbisvQWlDWDJzcnBnWDZLVmRHN1dFU0FNT1g4dz0='
                      '$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&ot=10%'
                      '2f26%2f2022%2017%3a36%3a44; LID=WEEvREcwSlJHSldSdmVpbisvQWlDWDJzcnBnWDZLVmRHN1dFU0FNT1g4dz0='
                      '$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; c_m_expire=2022-10-26%'
                      '2017%3a36%3a44; Ecp_session=1; Ecp_loginuserbk=XN0047; knsLeftGroupSelectItem=1%'
                      '3B2%3B; Ecp_ClientIp=117.172.232.165',
            'Sec-Fetch-Dest': ' empty',
            'Sec-Fetch-Mode': ' cors',
            'Sec-Fetch-Site': ' same-origin',
            'Content-Type': ' application/x-www-form-urlencoded; charset=UTF-8'
        }
        conn.request("POST", "/kns8/Brief/GetGridTableHtml", payload, headers)
        res = conn.getresponse()
        data = res.read()
        res_data = data.decode("utf-8")
        find_url = re.compile(r'<a class="fz14" href=\'(.*?)\' .*?</a>')
        """
        <a class="fz14" href="xxx" target="_blank" one-link-mark="yes">基于PT＿MA理论的共享制造机会主义共享行为<font class="Mark">演化博弈</font>分析</a>
        <a class="fz14" href=\'(.*?)\' .*?</a>
        """
        data_url_temp = re.findall(find_url, res_data)
        # print(f"(当前页有{len(data_url_temp)}篇文章)")
        if index in range(len(data_url_temp)):
            temp = data_url_temp[index]
            str_list = temp.split('&')
            page_url = f"https://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CAPJ&{str_list[4]}&{str_list[5]}"
            return page_url
        else:
            print(f"超过该页最大文章数量:{len(data_url_temp)}")
            exit()

    def get_page_info(self):
        url = self.url
        conn = http.client.HTTPSConnection("kns.cnki.net")
        payload = ''
        headers = {
            'Host': ' kns.cnki.net',
            'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
            'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': ' zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': ' keep-alive',
            'Cookie': ' cangjieStatus_NZKPT2=true; cangjieConfig_NZKPT2=%7B%22status%22%3Atrue%2C%22startTime%22%3A%222022-10-20%22%2C%22endTime%22%3A%222023-10-20%22%2C%22orginHosts%22%3A%22kns.cnki.net%22%2C%22type%22%3A%22mix%22%2C%22poolSize%22%3A%2210%22%2C%22intervalTime%22%3A10000%2C%22persist%22%3Afalse%7D; Ecp_notFirstLogin=OC6lZS; _pk_id=0a637184-eb1d-4c77-9a8c-d13f788f4b70.1666772312.1.1666773138.1666772312.; _pk_ref=%5B%22%22%2C%22%22%2C1666772312%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DRkL9J16nXRcfF_omFFvMbIh74gXh2W7oE44uvnJrPFW%26wd%3D%26eqid%3Da67f19810002aad8000000036358ed4e%22%5D; Ecp_ClientId=a221026161802477663; Ecp_loginuserbk=XN0047; knsLeftGroupSelectItem=1%3B2%3B; Ecp_ClientIp=117.172.232.165; SID_sug=126003; ASP.NET_SessionId=p5m4o3xrlg11vbb2dzxod5y0; SID_kns8=123154; dblang=ch; CurrSortField=%e7%9b%b8%e5%85%b3%e5%ba%a6%2frelevant%2c(%e5%8f%91%e8%a1%a8%e6%97%b6%e9%97%b4%2c%27time%27)+desc; CurrSortFieldType=desc; SID_kns_new=kns25128004; SID_docpre=128007; SID_kcms=025126024; Ecp_session=1; SID_kns=126007; Ecp_LoginStuts={"IsAutoLogin":false,"UserName":"XN0047","ShowName":"%E5%9B%9B%E5%B7%9D%E5%B8%88%E8%8C%83%E5%A4%A7%E5%AD%A6","UserType":"bk","BUserName":"","BShowName":"","BUserType":"","r":"OC6lZS","Members":[]}; c_m_LinID=LinID=WEEvREcwSlJHSldSdmVpbisvQWlDQW1sU21vRE5GaGdXQ1ZLNU5SWFhDaz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&ot=11%2F10%2F2022%2023%3A18%3A46; LID=WEEvREcwSlJHSldSdmVpbisvQWlDQW1sU21vRE5GaGdXQ1ZLNU5SWFhDaz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!; c_m_expire=2022-11-10%2023%3A18%3A46',
            'Upgrade-Insecure-Requests': ' 1',
            'Sec-Fetch-Dest': ' document',
            'Sec-Fetch-Mode': ' navigate',
            'Sec-Fetch-Site': ' none',
            'Sec-Fetch-User': ' ?1'
        }
        conn.request("GET", url, payload, headers)
        res = conn.getresponse()
        data = res.read()
        res_data = data.decode("utf-8")
        return res_data

    def get_title(self):
        """
        标题
        :return:
        """
        html = self.html
        find_element = re.compile(r'<h1>(.*?)<')
        data_url_temp = re.findall(find_element, html)
        return data_url_temp[0]

    def get_time(self):
        """
        发布时间
        :return:
        """
        html = self.html
        find_element = re.compile(r'<div class="head-time"><span>(.*?)</span></div>')
        data_url_temp = re.findall(find_element, html)
        if data_url_temp:
            return data_url_temp[0][data_url_temp[0].find("：")+1:]
        else:
            return None

    def get_author(self):
        """
        作者
        :return:
        """
        html = self.html
        authors_element = re.compile(r'<span><a target="_blank" onclick=".*?</span>')
        data_url_temp = re.findall(authors_element, html)
        authors = []
        for item in data_url_temp:
            author_element = re.compile(r"'au','(.*?)','")
            data_url_temp = re.findall(author_element, item)
            authors.append(data_url_temp[0])
        return authors

    def get_Work_unit(self):
        """
        工作单位
        :return:
        """
        html = self.html
        find_element = re.compile(r"'in','(.*?)','")
        data_url_temp = re.findall(find_element, html)
        return data_url_temp[0]

    def get_abstract(self):
        """
        摘要
        :return:
        """
        html = self.html
        find_element = re.compile(r'class="abstract-text">(.*?)</span>')
        data_url_temp = re.findall(find_element, html)
        return data_url_temp[0]

    def get_keyword(self):
        """
        关键词
        :return:
        """
        html = self.html
        soup = BeautifulSoup(html, 'lxml')
        a_tags = soup.find_all('p')
        keywords = []
        for item in a_tags:
            keyword = re.findall(re.compile(r"'kw','(.*?)',"), str(item))
            if keyword:
                keywords = keyword
        return keywords


if __name__ == '__main__':
    article = YanHuaBoYi(
        page=int(input(f"请输入页数:")),
        index=int(input(f"请输入文章序号:")),
        article_type=1
    )
    print(f"文章链接:{article.url}")
    print(f"发布时间:{article.get_time()}")
    print(f"标题:{article.get_title()}")
    print(f"作者:{article.get_author()}")
    print(f"机构:{article.get_Work_unit()}")
    print(f"关键词:{article.get_keyword()}")
    print(f"摘要:{article.get_abstract()}")
