import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from arxiv_api_integration_ai_connect import answer
from article_section_summary import get_context_and_feedback_from_ai


def pdf_download(pdf_link, article_title):
    # 根据返回的PDF下载连接，下载 PDF 文件
    pdf_filename = article_title + ".pdf"
    urllib.request.urlretrieve(pdf_link, pdf_filename)
    
    

def arxiv_api_calling(article_title, translation):
    # 定义参数

    method_name = "query"
    start = 0
    max_results = 30

    # 对参数进行编码
    encoded_article_title = urllib.parse.quote(article_title)

    # 构建有效的 URL
    url = f"http://export.arxiv.org/api/{method_name}?search_query={encoded_article_title}&start={start}&max_results={max_results}"

    # 获取数据
    response = urllib.request.urlopen(url)
    data = response.read().decode('utf-8')

    # print(data)

    # 解析 XML 数据
    root = ET.fromstring(data)

    # 提取文章信息
    article = {}
    for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):

        if entry.find('{http://www.w3.org/2005/Atom}title').text == article_title:

            # # Print the XML data，调试
            # print(ET.tostring(entry, encoding='utf-8').decode('utf-8'))

            article['id'] = entry.find('{http://www.w3.org/2005/Atom}id').text

            updated = entry.find('{http://www.w3.org/2005/Atom}updated').text
            article['updated'] = updated[:10] # 只保留日期部分

            published = entry.find('{http://www.w3.org/2005/Atom}published').text
            article['published'] = published[:10] 

            article['title'] = entry.find('{http://www.w3.org/2005/Atom}title').text
            article['summary'] = entry.find('{http://www.w3.org/2005/Atom}summary').text
            
            authors = entry.findall('{http://www.w3.org/2005/Atom}author')
            article['authors'] = [author.find('{http://www.w3.org/2005/Atom}name').text for author in authors]
            
            pdf_link = entry.find('{http://www.w3.org/2005/Atom}link[@title="pdf"]')
            if pdf_link is not None:
                article['pdf_link'] = pdf_link.attrib['href']
            
    summarized_article = answer(article['summary'], translation)
    article['summarized summary'] = summarized_article

    # 调用函数，下载 PDF 文件
    try:
        pdf_download(article.get('pdf_link'),article['title'])
        print(f"PDF downloaded successfully as {article['title']}.pdf .")
    except Exception as e:
        raise Exception(f"Download Fail: {e}")


    return article




# 调用函数
article_title = "Self-Modeling Based Diagnosis of Software-Defined Networks"
translation = "English"
article = arxiv_api_calling(article_title, translation)

# 打印文章信息
print(f"ID: {article['id']}")
print(f"Published: {article['published']}")
print(f"Updated: {article['updated']}")
print(f"Title: {article['title']}")
print(f"Summary: {article['summary']}")
print(f"Authors: {', '.join(article['authors'])}")
print(f"PDF Link: {article.get('pdf_link', 'N/A')}\n")
print(f"Summarized Summary: {article.get('summarized summary')}\n")

# Section B
output_dict = get_context_and_feedback_from_ai(article['title'], article['title'], translation = "English")
print("现在开始输出zzh的结果：")
output_text = output_dict['texts']
print(output_text)
output_summaries = output_dict['summaries']
print(output_summaries)
output_relatedwork = output_dict['Related work']
print(output_relatedwork)
output_logic = output_dict['Logical Chain']
print(output_logic)