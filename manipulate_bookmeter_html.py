from bs4 import BeautifulSoup
import re
import copy
# import pyperclip as pc

import pytest

def add_p_tag_to_plaintext(soup : BeautifulSoup) -> BeautifulSoup:
    impressions = soup.find_all(string=re.compile("\n"))
    for i in range(0, len(impressions)):
        tmp_soup = BeautifulSoup("", "html.parser")
        if i not in (0, len(impressions) - 1):
            sentences = impressions[i].split("\n")
            for j in range(0, len(sentences)):
                new_p = soup.new_tag("p")
                new_p.string = str(sentences[j])
                tmp_soup.append(new_p)
            impressions[i].replace_with(tmp_soup)
    return soup

def edit_style_of_img_and_wrap_by_figure(soup : BeautifulSoup, attrs_of_figure : dict) -> BeautifulSoup:
    images = soup.find_all("img")
    for element in images:
        element.attrs["style"] = "margin: 0 20px 5px 0; border: 1px solid #dcdcdc;"
        element.parent.replace_with(element) # remove <a> tag
        new_figure = soup.new_tag("figure", attrs=attrs_of_figure)
        element.wrap(new_figure)
    return soup

def add_ul_tag_about_dates_and_author(soup : BeautifulSoup) -> BeautifulSoup:
    read_dates = soup.find_all(string=re.compile("読了日"))
    for i in range(0, len(read_dates)):
        a_for_author = read_dates[i].find_next("a")
        list_of_date_and_author = read_dates[i].split(" ")

        new_li_for_date = soup.new_tag("li")
        new_li_for_date.string = list_of_date_and_author[0]

        new_li_for_author = soup.new_tag("li")
        new_a_for_author = soup.new_tag("a")
        new_a_for_author.string = list_of_date_and_author[1]
        preexist_a_for_author = copy.deepcopy(a_for_author)
        new_li_for_author.append(new_a_for_author)
        new_li_for_author.append(preexist_a_for_author)

        tmp_soup_date_and_author = soup.new_tag("ul")
        tmp_soup_date_and_author.append(new_li_for_date)
        tmp_soup_date_and_author.append(new_li_for_author)

        a_for_author.extract()
        read_dates[i].replace_with(tmp_soup_date_and_author)

    return soup

def remove_word_in_soup(soup : BeautifulSoup, pattern : str) -> BeautifulSoup:
    raw_no_strings = soup.find_all(string=re.compile(pattern))
    for string_element in raw_no_strings:
        string_element.extract()
    return soup

def add_h3_tag(soup : BeautifulSoup) -> BeautifulSoup:
    # add <h3> to title with impression
    impression_titles = soup.find_all("a", string=re.compile("感想"))
    for i in range(0, len(impression_titles)):
        preexist_a_for_title_2 = copy.deepcopy(impression_titles[i])
        new_a_for_no = soup.new_tag("a")
        new_a_for_no.string = "の"
        a_for_title = impression_titles[i].find_previous("a")
        preexist_a_for_title_1 = copy.deepcopy(a_for_title)

        new_h3_for_title = soup.new_tag("h3")
        new_h3_for_title.append(preexist_a_for_title_1)
        new_h3_for_title.append(new_a_for_no)
        new_h3_for_title.append(preexist_a_for_title_2)

        a_for_title.extract()
        impression_titles[i].replace_with(new_h3_for_title)
 
    # add <h3> to title without impression
    a_titles = soup.find_all("a")
    for i in range(0, len(a_titles)):
        if i not in (0, len(a_titles) - 1):
            if type(a_titles[i].parent) == BeautifulSoup:
                a_titles[i].wrap(soup.new_tag("h3"))

    return soup

def add_h2_tag(soup : BeautifulSoup) -> BeautifulSoup:
    a_title_for_h2 = soup.find("a")
    a_title_for_h2.wrap(soup.new_tag("h2"))
    return soup

def add_ul_tag_about_beginning(soup : BeautifulSoup) -> BeautifulSoup:
    limit_of_beginning = 6
    count_of_beginning = 0
    list_of_index_to_remove_strings = []
    # create <ul> contents
    new_ul_for_beginning = soup.new_tag("ul")
    for string in soup.strings:
        count_of_beginning += 1
        if count_of_beginning in (1, 2):
            continue
        if count_of_beginning >= limit_of_beginning:
            break
        new_li_for_beginning = soup.new_tag("li")
        new_li_for_beginning.append(copy.deepcopy(string))
        new_ul_for_beginning.append(new_li_for_beginning)
        list_of_index_to_remove_strings.append(count_of_beginning)
    # remove strings not required
    list_of_index_to_remove_strings_copied = copy.deepcopy(list_of_index_to_remove_strings)
    for i in list_of_index_to_remove_strings_copied:
        tmp_soup_strings = soup.strings
        count_of_beginning = 0
        for string in tmp_soup_strings:
            count_of_beginning += 1
            if count_of_beginning in (1, 2):
                continue
            if count_of_beginning == list_of_index_to_remove_strings[len(list_of_index_to_remove_strings) - 1]:
                string.extract()
                list_of_index_to_remove_strings.pop()
                break
    soup.find("h2").insert_after(new_ul_for_beginning)
    brs = soup.find_all("br")
    removing_count = len(list_of_index_to_remove_strings_copied) + 1
    for i in range(0, removing_count):
        brs[i].extract()
    
    return soup

def move_tag_to_behind(soup : BeautifulSoup, moving_tag : str, destination_tag : str) -> BeautifulSoup:
    figures = soup.find_all(moving_tag)
    for i in range(0, len(figures)):
        figure_copied = copy.deepcopy(figures[i])
        figures[i].find_next(destination_tag).insert_after(figure_copied)
        figures[i].extract()
    return soup

def generate_bookmeter_blogcard_by_a_tag(a_tag, bookmeter_id : str, title_of_blogcard : str):
    """
    a_tag : bs4.element.Tag
    return : bs4.element.Tag
    """
    soup = BeautifulSoup("", "html.parser")

    a_tag.attrs["href"] = a_tag.attrs["href"] + f"{bookmeter_id}"
    a_tag.attrs["rel"] = "noopener"
    a_tag.attrs["target"] = "_blank"
    a_tag.attrs["title"] = title_of_blogcard
    a_tag.attrs["class"] = "blogcard-wrap external-blogcard-wrap a-wrap cf"
    a_tag.string = ""

    blog_card = soup.new_tag("div", attrs={"class": "blogcard external-blogcard eb-left cf"})
    part_1 = soup.new_tag("div", attrs={"class": "blogcard-label external-blogcard-label"})
    part_1.append(soup.new_tag("span", attrs={"class": "fa"}))
    part_2 = soup.new_tag("figure", attrs={"class": "blogcard-thumbnail external-blogcard-thumbnail"})
    part_2_1 = soup.new_tag("img", attrs={
        "src": "https://www.endorphinbath.com/wp-content/uploads/cocoon-resources/blog-card-cache/1383df5cdd9020df38904c80c880706d.png"
        , "class": "blogcard-thumb-image external-blogcard-thumb-image"
        , "width": "160"
        , "height": "90"
        , "alt": ""
    })
    part_2.append(part_2_1)
    part_3 = soup.new_tag("div", attrs={"class": "blogcard-content external-blogcard-content"})
    part_3_1 = soup.new_tag("div", attrs={"class": "blogcard-title external-blogcard-title"})
    part_3_1.string = title_of_blogcard
    part_3_2 = soup.new_tag("div", attrs={"class": "blogcard-snippet external-blogcard-snippet"})
    part_3.append(part_3_1)
    part_3.append(part_3_2)
    part_4 = soup.new_tag("div", attrs={"class": "blogcard-footer external-blogcard-footer cf"})
    part_4_1 = soup.new_tag("div", attrs={"class": "blogcard-site external-blogcard-site"})
    part_4_1_1 = soup.new_tag("div", attrs={"class": "blogcard-favicon external-blogcard-favicon"})
    part_4_1_1_1 = soup.new_tag("img", attrs={
        "src": "https://www.google.com/s2/favicons?domain=https://bookmeter.com/users/1313175"
        , "class": "blogcard-favicon-image external-blogcard-favicon-image"
        , "width": "16"
        , "height": "16"
        , "alt": ""
    })
    part_4_1_1.append(part_4_1_1_1)
    part_4_1_2 = soup.new_tag("div", attrs={"class": "blogcard-domain external-blogcard-domain"})
    part_4_1_2.string = "bookmeter.com"
    part_4_1.append(part_4_1_1)
    part_4_1.append(part_4_1_2)
    part_4.append(part_4_1)
    blog_card.append(part_1)
    blog_card.append(part_2)
    blog_card.append(part_3)
    blog_card.append(part_4)
    return blog_card

def generate_bookmeter_blogcard(soup : BeautifulSoup, bookmeter_id : str, title_of_blogcard : str) -> BeautifulSoup:
    bsset_a = soup.find_all("a")
    link_of_bookmeter = bsset_a[len(bsset_a) - 1]
    blog_card = generate_bookmeter_blogcard_by_a_tag(link_of_bookmeter, bookmeter_id, title_of_blogcard)
    link_of_bookmeter.append(blog_card)
    return soup

def manipulate_bookmeter_html(target_html : str) -> BeautifulSoup:
    soup = BeautifulSoup(target_html, "html.parser")

    soup = add_p_tag_to_plaintext(soup)
    soup = edit_style_of_img_and_wrap_by_figure(soup, {"class": "wp-block-image size-large"})
    soup = add_ul_tag_about_dates_and_author(soup)
    
    # Execution adding <h3>: start -------------------------------------------------------------------
    soup = remove_word_in_soup(soup, r"^の$")
    soup = add_h3_tag(soup)
    # Execution adding <h3>: end -------------------------------------------------------------------

    soup = add_h2_tag(soup)
    soup = add_ul_tag_about_beginning(soup)
    soup = move_tag_to_behind(soup, "figure", "h3")

    my_bookmeter_id = "users/1313175"
    title_of_blogcard = "kinkinbeer135ml - 読書メーター"
    soup = generate_bookmeter_blogcard(soup, my_bookmeter_id, title_of_blogcard)

    return soup

def main():
    bookmeter_html = """
<a href="https://bookmeter.com/users/1313175/summary/monthly/2022/2">2月の読書メーター</a><br>読んだ本の数：5<br>読んだページ数：1998<br>ナイス数：1<br><br><a href="https://bookmeter.com/books/8189791"><img alt="人生は20代で決まる" align="left" style="margin: 0 5px 5px 0; border: 1px solid #dcdcdc;" src="https://m.media-amazon.com/images/I/41z9XyhfOLL._SL75_.jpg"></a><a href="https://bookmeter.com/books/8189791?title=%E4%BA%BA%E7%94%9F%E3%81%AF20%E4%BB%A3%E3%81%A7%E6%B1%BA%E3%81%BE%E3%82%8B">人生は20代で決まる</a>の<a href="https://bookmeter.com/reviews/104504909">感想</a><br>本書の進行形式として、色々な人の人生設計を具体的にどのようにより良いものにしていくかどうかを1つずつケーススタディしていく流れである。
僕が本書から汲み取ったことは、目標を立てて行動し、若い内にとっととその目標を実現できるように行動していこう、ということである。
特に、結婚して子作りすることにおいては、年齢が重要な要素になってくるため、長期的な目標は子作りよりも早く実現もしくは形にできるように人生設計を行っていかなくてはならない。<br>読了日：02月14日 著者：<a href="https://bookmeter.com/search?keyword=%E3%83%A1%E3%82%B0+%E3%82%B8%E3%82%A7%E3%82%A4%2CMeg+Jay">メグ ジェイ,Meg Jay</a><br clear="left"><a href="https://bookmeter.com/books/11185007"><img alt="沈黙のWebライティング —Webマーケッター ボーンの激闘—〈SEOのためのライティング教本〉" align="left" style="margin: 0 5px 5px 0; border: 1px solid #dcdcdc;" src="https://m.media-amazon.com/images/I/51TvUiUY+tL._SL75_.jpg"></a><a href="https://bookmeter.com/books/11185007?title=%E6%B2%88%E9%BB%99%E3%81%AEWeb%E3%83%A9%E3%82%A4%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0+%E2%80%94Web%E3%83%9E%E3%83%BC%E3%82%B1%E3%83%83%E3%82%BF%E3%83%BC+%E3%83%9C%E3%83%BC%E3%83%B3%E3%81%AE%E6%BF%80%E9%97%98%E2%80%94%E3%80%88SEO%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%A9%E3%82%A4%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0%E6%95%99%E6%9C%AC%E3%80%89">沈黙のWebライティング —Webマーケッター ボーンの激闘—〈SEOのためのライティング教本〉</a>の<a href="https://bookmeter.com/reviews/104294763">感想</a><br>自分のブログへ何か参考できないかどうか興味があり読んでみました。
漫画になっていたり、所々必殺技みたいなものが展開されたり、分かりやすく楽しんで読むことができました。
SEOなど実践してみたいと思います。<br>読了日：02月06日 著者：<a href="https://bookmeter.com/search?keyword=%E6%9D%BE%E5%B0%BE+%E8%8C%82%E8%B5%B7">松尾 茂起</a><br clear="left"><a href="https://bookmeter.com/books/11884421"><img alt="MIND OVER MONEY 193の心理研究でわかったお金に支配されない13の真実" align="left" style="margin: 0 5px 5px 0; border: 1px solid #dcdcdc;" src="https://m.media-amazon.com/images/I/51y8GIycbyL._SL75_.jpg"></a><a href="https://bookmeter.com/books/11884421?title=MIND+OVER+MONEY+193%E3%81%AE%E5%BF%83%E7%90%86%E7%A0%94%E7%A9%B6%E3%81%A7%E3%82%8F%E3%81%8B%E3%81%A3%E3%81%9F%E3%81%8A%E9%87%91%E3%81%AB%E6%94%AF%E9%85%8D%E3%81%95%E3%82%8C%E3%81%AA%E3%81%8413%E3%81%AE%E7%9C%9F%E5%AE%9F">MIND OVER MONEY 193の心理研究でわかったお金に支配されない13の真実</a><br>読了日：02月06日 著者：<a href="https://bookmeter.com/search?keyword=%E3%82%AF%E3%83%A9%E3%82%A6%E3%83%87%E3%82%A3%E3%82%A2%E3%83%BB%E3%83%8F%E3%83%A2%E3%83%B3%E3%83%89">クラウディア・ハモンド</a><br clear="left"><a href="https://bookmeter.com/books/17071653"><img alt="シゴトがはかどる Python自動処理の教科書" align="left" style="margin: 0 5px 5px 0; border: 1px solid #dcdcdc;" src="https://m.media-amazon.com/images/I/51gFnBtbrWL._SL75_.jpg"></a><a href="https://bookmeter.com/books/17071653?title=%E3%82%B7%E3%82%B4%E3%83%88%E3%81%8C%E3%81%AF%E3%81%8B%E3%81%A9%E3%82%8B+Python%E8%87%AA%E5%8B%95%E5%87%A6%E7%90%86%E3%81%AE%E6%95%99%E7%A7%91%E6%9B%B8">シゴトがはかどる Python自動処理の教科書</a>の<a href="https://bookmeter.com/reviews/104275292">感想</a><br>Pythonの入門編といった感じの一冊となっている。Excelの処理が多め。個人的にはダウンロード処理とメール送信処理の部分を行ったことがないので、今度試してみようと思う。<br>読了日：02月05日 著者：<a href="https://bookmeter.com/search?keyword=%E3%82%AF%E3%82%B8%E3%83%A9%E9%A3%9B%E8%A1%8C%E6%9C%BA">クジラ飛行机</a><br clear="left"><a href="https://bookmeter.com/books/11204117"><img alt="新装版 達人プログラマー 職人から名匠への道" align="left" style="margin: 0 5px 5px 0; border: 1px solid #dcdcdc;" src="https://m.media-amazon.com/images/I/51aDNpMj8hL._SL75_.jpg"></a><a href="https://bookmeter.com/books/11204117?title=%E6%96%B0%E8%A3%85%E7%89%88+%E9%81%94%E4%BA%BA%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9E%E3%83%BC+%E8%81%B7%E4%BA%BA%E3%81%8B%E3%82%89%E5%90%8D%E5%8C%A0%E3%81%B8%E3%81%AE%E9%81%93">新装版 達人プログラマー 職人から名匠への道</a><br>読了日：02月05日 著者：<a href="https://bookmeter.com/search?keyword=Andrew+Hunt%2CDavid+Thomas">Andrew Hunt,David Thomas</a><br clear="left"><br><a href="https://bookmeter.com/">読書メーター</a><br>
"""
    soup = manipulate_bookmeter_html(bookmeter_html)
    print("======================= prettify start ===========================")
    print(soup.prettify())
    # pc.copy(soup.prettify())
    # print("copied to your clipboard!")
    print("======================= prettify end ===========================")

# main()


# test: start -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def test_manipulate_bookmeter_html_1_1():
    bookmeter_html = """
<a href="https://bookmeter.com/users/1313175/summary/monthly/2022/2">2月の読書メーター</a><br>読んだ本の数：5<br>読んだページ数：1998<br>ナイス数：1<br><br><a href="https://bookmeter.com/books/8189791"><img alt="人生は20代で決まる" align="left" style="margin: 0 5px 5px 0; border: 1px solid #dcdcdc;" src="https://m.media-amazon.com/images/I/41z9XyhfOLL._SL75_.jpg"></a><a href="https://bookmeter.com/books/8189791?title=%E4%BA%BA%E7%94%9F%E3%81%AF20%E4%BB%A3%E3%81%A7%E6%B1%BA%E3%81%BE%E3%82%8B">人生は20代で決まる</a>の<a href="https://bookmeter.com/reviews/104504909">感想</a><br>本書の進行形式として、色々な人の人生設計を具体的にどのようにより良いものにしていくかどうかを1つずつケーススタディしていく流れである。
僕が本書から汲み取ったことは、目標を立てて行動し、若い内にとっととその目標を実現できるように行動していこう、ということである。
特に、結婚して子作りすることにおいては、年齢が重要な要素になってくるため、長期的な目標は子作りよりも早く実現もしくは形にできるように人生設計を行っていかなくてはならない。<br>読了日：02月14日 著者：<a href="https://bookmeter.com/search?keyword=%E3%83%A1%E3%82%B0+%E3%82%B8%E3%82%A7%E3%82%A4%2CMeg+Jay">メグ ジェイ,Meg Jay</a><br clear="left"><a href="https://bookmeter.com/books/11185007"><img alt="沈黙のWebライティング —Webマーケッター ボーンの激闘—〈SEOのためのライティング教本〉" align="left" style="margin: 0 5px 5px 0; border: 1px solid #dcdcdc;" src="https://m.media-amazon.com/images/I/51TvUiUY+tL._SL75_.jpg"></a><a href="https://bookmeter.com/books/11185007?title=%E6%B2%88%E9%BB%99%E3%81%AEWeb%E3%83%A9%E3%82%A4%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0+%E2%80%94Web%E3%83%9E%E3%83%BC%E3%82%B1%E3%83%83%E3%82%BF%E3%83%BC+%E3%83%9C%E3%83%BC%E3%83%B3%E3%81%AE%E6%BF%80%E9%97%98%E2%80%94%E3%80%88SEO%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%A9%E3%82%A4%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0%E6%95%99%E6%9C%AC%E3%80%89">沈黙のWebライティング —Webマーケッター ボーンの激闘—〈SEOのためのライティング教本〉</a>の<a href="https://bookmeter.com/reviews/104294763">感想</a><br>自分のブログへ何か参考できないかどうか興味があり読んでみました。
漫画になっていたり、所々必殺技みたいなものが展開されたり、分かりやすく楽しんで読むことができました。
SEOなど実践してみたいと思います。<br>読了日：02月06日 著者：<a href="https://bookmeter.com/search?keyword=%E6%9D%BE%E5%B0%BE+%E8%8C%82%E8%B5%B7">松尾 茂起</a><br clear="left"><a href="https://bookmeter.com/books/11884421"><img alt="MIND OVER MONEY 193の心理研究でわかったお金に支配されない13の真実" align="left" style="margin: 0 5px 5px 0; border: 1px solid #dcdcdc;" src="https://m.media-amazon.com/images/I/51y8GIycbyL._SL75_.jpg"></a><a href="https://bookmeter.com/books/11884421?title=MIND+OVER+MONEY+193%E3%81%AE%E5%BF%83%E7%90%86%E7%A0%94%E7%A9%B6%E3%81%A7%E3%82%8F%E3%81%8B%E3%81%A3%E3%81%9F%E3%81%8A%E9%87%91%E3%81%AB%E6%94%AF%E9%85%8D%E3%81%95%E3%82%8C%E3%81%AA%E3%81%8413%E3%81%AE%E7%9C%9F%E5%AE%9F">MIND OVER MONEY 193の心理研究でわかったお金に支配されない13の真実</a><br>読了日：02月06日 著者：<a href="https://bookmeter.com/search?keyword=%E3%82%AF%E3%83%A9%E3%82%A6%E3%83%87%E3%82%A3%E3%82%A2%E3%83%BB%E3%83%8F%E3%83%A2%E3%83%B3%E3%83%89">クラウディア・ハモンド</a><br clear="left"><a href="https://bookmeter.com/books/17071653"><img alt="シゴトがはかどる Python自動処理の教科書" align="left" style="margin: 0 5px 5px 0; border: 1px solid #dcdcdc;" src="https://m.media-amazon.com/images/I/51gFnBtbrWL._SL75_.jpg"></a><a href="https://bookmeter.com/books/17071653?title=%E3%82%B7%E3%82%B4%E3%83%88%E3%81%8C%E3%81%AF%E3%81%8B%E3%81%A9%E3%82%8B+Python%E8%87%AA%E5%8B%95%E5%87%A6%E7%90%86%E3%81%AE%E6%95%99%E7%A7%91%E6%9B%B8">シゴトがはかどる Python自動処理の教科書</a>の<a href="https://bookmeter.com/reviews/104275292">感想</a><br>Pythonの入門編といった感じの一冊となっている。Excelの処理が多め。個人的にはダウンロード処理とメール送信処理の部分を行ったことがないので、今度試してみようと思う。<br>読了日：02月05日 著者：<a href="https://bookmeter.com/search?keyword=%E3%82%AF%E3%82%B8%E3%83%A9%E9%A3%9B%E8%A1%8C%E6%9C%BA">クジラ飛行机</a><br clear="left"><a href="https://bookmeter.com/books/11204117"><img alt="新装版 達人プログラマー 職人から名匠への道" align="left" style="margin: 0 5px 5px 0; border: 1px solid #dcdcdc;" src="https://m.media-amazon.com/images/I/51aDNpMj8hL._SL75_.jpg"></a><a href="https://bookmeter.com/books/11204117?title=%E6%96%B0%E8%A3%85%E7%89%88+%E9%81%94%E4%BA%BA%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9E%E3%83%BC+%E8%81%B7%E4%BA%BA%E3%81%8B%E3%82%89%E5%90%8D%E5%8C%A0%E3%81%B8%E3%81%AE%E9%81%93">新装版 達人プログラマー 職人から名匠への道</a><br>読了日：02月05日 著者：<a href="https://bookmeter.com/search?keyword=Andrew+Hunt%2CDavid+Thomas">Andrew Hunt,David Thomas</a><br clear="left"><br><a href="https://bookmeter.com/">読書メーター</a><br>
"""
    actual = manipulate_bookmeter_html(bookmeter_html)
    expected_html = """
<h2><a href="https://bookmeter.com/users/1313175/summary/monthly/2022/2">2月の読書メーター</a></h2><ul><li>読んだ本の数：5</li><li>読んだページ数：1998</li><li>ナイス数：1</li></ul><br/><h3><a href="https://bookmeter.com/books/8189791?title=%E4%BA%BA%E7%94%9F%E3%81%AF20%E4%BB%A3%E3%81%A7%E6%B1%BA%E3%81%BE%E3%82%8B">人生は20代で決まる</a><a>の</a><a href="https://bookmeter.com/reviews/104504909">感想</a></h3><figure class="wp-block-image size-large"><img align="left" alt="人生は20代で決まる" src="https://m.media-amazon.com/images/I/41z9XyhfOLL._SL75_.jpg" style="margin: 0 20px 5px 0; border: 1px solid #dcdcdc;"/></figure><br/><p>本書の進行形式として、色々な人の人生設計を具体的にどのようにより良いものにしていくかどうかを1つずつケーススタディしていく流れである。</p><p>僕が本書から汲み取ったことは、目標を立てて行動し、若い内にとっととその目標を実現できるように行動していこう、ということである。</p><p>特に、結婚して子作りすることにおいては、年齢が重要な要素になってくるため、長期的な目標は子作りよりも早く実現もしくは形にできるように人生設計を行っていかなくてはならない。</p><br/><ul><li>読了日：02月14日</li><li><a>著者：</a><a href="https://bookmeter.com/search?keyword=%E3%83%A1%E3%82%B0+%E3%82%B8%E3%82%A7%E3%82%A4%2CMeg+Jay">メグ ジェイ,Meg Jay</a></li></ul><br clear="left"/><h3><a href="https://bookmeter.com/books/11185007?title=%E6%B2%88%E9%BB%99%E3%81%AEWeb%E3%83%A9%E3%82%A4%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0+%E2%80%94Web%E3%83%9E%E3%83%BC%E3%82%B1%E3%83%83%E3%82%BF%E3%83%BC+%E3%83%9C%E3%83%BC%E3%83%B3%E3%81%AE%E6%BF%80%E9%97%98%E2%80%94%E3%80%88SEO%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%A9%E3%82%A4%E3%83%86%E3%82%A3%E3%83%B3%E3%82%B0%E6%95%99%E6%9C%AC%E3%80%89">沈黙のWebライティング —Webマーケッター ボーンの激闘—〈SEOのためのライティング教本〉</a><a>の</a><a href="https://bookmeter.com/reviews/104294763">感想</a></h3><figure class="wp-block-image size-large"><img align="left" alt="沈黙のWebライティング —Webマーケッター ボーンの激闘—〈SEOのためのライティング教本〉" src="https://m.media-amazon.com/images/I/51TvUiUY+tL._SL75_.jpg" style="margin: 0 20px 5px 0; border: 1px solid #dcdcdc;"/></figure><br/><p>自分のブログへ何か参考できないかどうか興味があり読んでみました。</p><p>漫画になっていたり、所々必殺技みたいなものが展開されたり、分かりやすく楽しんで読むことができました。</p><p>SEOなど実践してみたいと思います。</p><br/><ul><li>読了日：02月06日</li><li><a>著者：</a><a href="https://bookmeter.com/search?keyword=%E6%9D%BE%E5%B0%BE+%E8%8C%82%E8%B5%B7">松尾 茂起</a></li></ul><br clear="left"/><h3><a href="https://bookmeter.com/books/11884421?title=MIND+OVER+MONEY+193%E3%81%AE%E5%BF%83%E7%90%86%E7%A0%94%E7%A9%B6%E3%81%A7%E3%82%8F%E3%81%8B%E3%81%A3%E3%81%9F%E3%81%8A%E9%87%91%E3%81%AB%E6%94%AF%E9%85%8D%E3%81%95%E3%82%8C%E3%81%AA%E3%81%8413%E3%81%AE%E7%9C%9F%E5%AE%9F">MIND OVER MONEY 193の心理研究でわかったお金に支配されない13の真実</a></h3><figure class="wp-block-image size-large"><img align="left" alt="MIND OVER MONEY 193の心理研究でわかったお金に支配されない13の真実" src="https://m.media-amazon.com/images/I/51y8GIycbyL._SL75_.jpg" style="margin: 0 20px 5px 0; border: 1px solid #dcdcdc;"/></figure><br/><ul><li>読了日：02月06日</li><li><a>著者：</a><a href="https://bookmeter.com/search?keyword=%E3%82%AF%E3%83%A9%E3%82%A6%E3%83%87%E3%82%A3%E3%82%A2%E3%83%BB%E3%83%8F%E3%83%A2%E3%83%B3%E3%83%89">クラウディア・ハモンド</a></li></ul><br clear="left"/><h3><a href="https://bookmeter.com/books/17071653?title=%E3%82%B7%E3%82%B4%E3%83%88%E3%81%8C%E3%81%AF%E3%81%8B%E3%81%A9%E3%82%8B+Python%E8%87%AA%E5%8B%95%E5%87%A6%E7%90%86%E3%81%AE%E6%95%99%E7%A7%91%E6%9B%B8">シゴトがはかどる Python自動処理の教科書</a><a>の</a><a href="https://bookmeter.com/reviews/104275292">感想</a></h3><figure class="wp-block-image size-large"><img align="left" alt="シゴトがはかどる Python自動処理の教科書" src="https://m.media-amazon.com/images/I/51gFnBtbrWL._SL75_.jpg" style="margin: 0 20px 5px 0; border: 1px solid #dcdcdc;"/></figure><br/>Pythonの入門編といった感じの一冊となっている。Excelの処理が多め。個人的にはダウンロード処理とメール送信処理の部分を行ったことがないので、今度試してみようと思う。<br/><ul><li>読了日：02月05日</li><li><a>著者：</a><a href="https://bookmeter.com/search?keyword=%E3%82%AF%E3%82%B8%E3%83%A9%E9%A3%9B%E8%A1%8C%E6%9C%BA">クジラ飛行机</a></li></ul><br clear="left"/><h3><a href="https://bookmeter.com/books/11204117?title=%E6%96%B0%E8%A3%85%E7%89%88+%E9%81%94%E4%BA%BA%E3%83%97%E3%83%AD%E3%82%B0%E3%83%A9%E3%83%9E%E3%83%BC+%E8%81%B7%E4%BA%BA%E3%81%8B%E3%82%89%E5%90%8D%E5%8C%A0%E3%81%B8%E3%81%AE%E9%81%93">新装版 達人プログラマー 職人から名匠への道</a></h3><figure class="wp-block-image size-large"><img align="left" alt="新装版 達人プログラマー 職人から名匠への道" src="https://m.media-amazon.com/images/I/51aDNpMj8hL._SL75_.jpg" style="margin: 0 20px 5px 0; border: 1px solid #dcdcdc;"/></figure><br/><ul><li>読了日：02月05日</li><li><a>著者：</a><a href="https://bookmeter.com/search?keyword=Andrew+Hunt%2CDavid+Thomas">Andrew Hunt,David Thomas</a></li></ul><br clear="left"/><br/><a class="blogcard-wrap external-blogcard-wrap a-wrap cf" href="https://bookmeter.com/users/1313175" rel="noopener" target="_blank" title="kinkinbeer135ml - 読書メーター"><div class="blogcard external-blogcard eb-left cf"><div class="blogcard-label external-blogcard-label"><span class="fa"></span></div><figure class="blogcard-thumbnail external-blogcard-thumbnail"><img alt="" class="blogcard-thumb-image external-blogcard-thumb-image" height="90" src="https://www.endorphinbath.com/wp-content/uploads/cocoon-resources/blog-card-cache/1383df5cdd9020df38904c80c880706d.png" width="160"/></figure><div class="blogcard-content external-blogcard-content"><div class="blogcard-title external-blogcard-title">kinkinbeer135ml - 読書メーター</div><div class="blogcard-snippet external-blogcard-snippet"></div></div><div class="blogcard-footer external-blogcard-footer cf"><div class="blogcard-site external-blogcard-site"><div class="blogcard-favicon external-blogcard-favicon"><img alt="" class="blogcard-favicon-image external-blogcard-favicon-image" height="16" src="https://www.google.com/s2/favicons?domain=https://bookmeter.com/users/1313175" width="16"/></div><div class="blogcard-domain external-blogcard-domain">bookmeter.com</div></div></div></div></a><br/>
"""
    expected = BeautifulSoup(expected_html, "html.parser")
    assert str(actual) == str(expected)

# test: end -----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
