# manipulate_bookmeter_html

<img width="20%" alt="" src="./img/01-01_logo.png">

## Usage

### 1. Get HTML from Book-meter web site.

[Here](https://bookmeter.com/users/1313175).

### 2. Make "Before" file

Visit "読書管理>まとめ>ブログでまとめる".

![](./img/02_01.jpg)

1. Copy HTML on the bottom.
2. Paste into new file in this repo folder: `history_of_before`.

![](./img/02_02.jpg)
### 3. Generate "After" file

Execute Github Actions: `Transform HTML`.

![](./img/02_03.jpg)

### 4. Done.

You'll find the blog article to post in `history_of_after` folder.

## Changelog

| When | Category | What | Why | Published |
|---|---|---|---|---|
|02-07-2023|Enhancement|Adds Github Actions.|To run with the browser.|Yes|
|02-07-2023|Fixed|Rewrites Jupyter Notebook to Python file.|Code had been cluttered.|Yes|
