## get-all-repository-grep

### 概要 / Overview
-It`s python script a file that all clone git repository on gitlab,
  and grep html/js/json/css files, also output to csv.
  
-pythonでgitlab上にあるすべてのレポジトリ情報を取得して、
  cloneしたディレクトリ内からHTML,JS,css拡張子のファイルを検索してcsvファイルに出力するスクリプト。

### 処理内容 / Flow

1. gitlab上のレポジトリ情報を取得<br>
   Clone all gitlab repository on "repo_dir/".
   
   
2. "repo_dir/"配下の各レポジトリディレクトリ内のhtml/js(json)/cssファイルを検索する<br>
   Grep .html/.js(json)/.css files each repository-directory("repo_dir/").
   
   
3. レポジトリ名とファイルパス、URLと正規表現で取得、置換する<br>
   It Regular-Expressed to repository-name, file-path, URL-path.
   
   
4. "(date)_csv_data/"配下にcsvファイルで出力する<br>
   Output to csv files on "(date)_csv_data/"
   


#### フォルダ構成(前提構成) / Directory composition

*# = 事前に作成するディレクトリ<br>
*# = create directory yourself

*date = yyyymmdd

```
├──(home directory)
└── repo_file_list.py
  └── #/git_repository_list/
     ├── repo_dir/
        ├── (repository_name01)
        ├── (repository_name02)
        ・
        ・
        ・
        └──(repository_name50)
    └──(date)_csv_data/
        ├── (date)_html.csv
        ├── (date)_js.csv
        └── (date)_css.csv
  ```
      
### Python Version
-Python 3.6.8

### 出力イメージ / Output image

・(date)_html.csv

![image](https://user-images.githubusercontent.com/48123158/152742673-59094ec8-9e5d-4c06-ad0d-9aefc5639e91.png)

