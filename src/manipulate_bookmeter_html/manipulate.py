# coding: UTF-8

# Library by default
import re
import copy
# Library by locatl
from config import get_config
# Library by third party
from bs4 import BeautifulSoup
import pyperclip as pc

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
