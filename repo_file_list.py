#!/usr/bin/python
# coding=utf-8
"""
python3をインストールしてある前提
linuxで実行する方法 : python3 ファイル名.py
"""

import csv
import datetime as dt
import glob
# from pathlib import Path
# import openpyxl
import os
import re
import subprocess
import sys

TOKEN = "access token" # gitlab:アクセストークン
TOKEN_CHAR = r'"' + "Private-Token: " + TOKEN + r'" '
GIT_PATH = "https://(gitpath/)?per_page=50" # 50レポジトリまで取得できるようにする
GETHTTP_PATH = " | " + "jq .[].http_url_to_repo" + " | " #http-clone パス抽出
REGEX_URL = r"sed -e 's/https:\/\//https:\/\/(username)):(password)" + " | " #ユーザー、パスワード入力を省略するための置換
CLONE_CMD = "xargs -n 1 git clone --depth=1"
CURL_CMD = TOKEN_CHAR + GIT_PATH + GETHTTP_PATH + REGEX_URL + CLONE_CMD
TODAY = (dt.datetime.now()).strftime('%Y%m%d') #今日の日付
REPOSITORY_DIR = 'git_repository_list/'
TARGET_DIR = REPOSITORY_DIR + 'repo_dir/'
RESULT_CSV_DIR = REPOSITORY_DIR + TODAY + '_csv_data/'

def get_repo():
    """
    ディレクトリを作成し、gitリポジトリ一覧を取得する
    """
    try:
        os.makedirs(TARGET_DIR, exist_ok=True)
        os.makedirs(RESULT_CSV_DIR, exist_ok=True)
        # ディレクトリ移動
        os.chdir(TARGET_DIR)

        # git clone 全リポジトリ実行
        subprocess.run('curl -sH' + CURL_CMD, shell=True)
        # homeディレクトリ移動
        os.chdir('../..')

    except FileExistsError:
        subprocess.run(['echo', 'クローンに失敗しました。アクセストークンの期限を確認してください'])
        pass


def glob_file():
    """
    ディレクトリ内を検索する
    """
    try:
        # ファイルパス取得
        file_path = name.replace(TARGET_DIR, '')

        # repositoryを抽出
        repository_name = re.match('^.*?(?=\/)', file_path)

        # content以下を抽出
        content_path = re.sub('^.*?(?=\/)', '', file_path)

        # URL置換
        url_path = re.sub('.+?jp', 'https://(domain_name))', file_path)

        # print( repository_name.group() )
        # print( content_path )
        # print( url_path )

        return repository_name.group(), content_path, url_path

    except FileExistsError:
        subprocess.run(['echo', 'ファイル検索に失敗しました。'])
        pass


def output_csv(file_extension):
    """
    必要情報をcsvに出力する
    """
    file_name = RESULT_CSV_DIR + TODAY + '_' + file_extension + '.csv'
    js_file_name = RESULT_CSV_DIR + TODAY + '_' + js + '.csv'

    # print( file_name )

    try:

        # json結果はjsのcsvにまとめる
        if file_extension == json:
            with open(js_file_name, "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(glob_file())

        else :
            with open(file_name, "a", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(glob_file())

    except FileExistsError:
        subprocess.run(['echo', 'CSV出力に失敗しました。'])
        pass


# def join_xls():
#     """
#     csvをExcelに結合する。
#     1csv=1シートへの変換
#     """
#     try:
#         csvfiles = glob.glob(RESULT_CSV_DIR + '*.csv', recursive=False)
#         wb = openpyxl.Workbook()
#         for file in csvfiles:
#             wb.create_sheet(os.path.splitext(os.path.basename(file))[0])
#             wb.active = wb.sheetnames.index(os.path.splitext(os.path.basename(file))[0])
#             ws = wb.active
#             with open(file, encoding="shift-jis") as f:
#                 reader = csv.reader(f, delimiter=',')
#                 for row in reader:
#                     ws.append(row)
#         wb.save(RESULT_CSV_DIR + TODAY + '_result_' + '.xls')
#         return

#     except FileExistsError:
#         subprocess.run(['echo', 'Excel結合に失敗しました。'])
#         pass


# repositroy_listディレクトリの存在確認
if os.path.exists(REPOSITORY_DIR):
    html = 'html'
    js = 'js'
    json = 'json'
    css = 'css'

    try:
        get_repo()

        for name in glob.glob(TARGET_DIR + '**/*.' + html, recursive=True):
            output_csv( html )
        
        for name in glob.glob(TARGET_DIR + '**/*.' + js, recursive=True):
            output_csv( js )
        
        for name in glob.glob(TARGET_DIR + '**/*.' + json, recursive=True):
            output_csv( json )
        
        for name in glob.glob(TARGET_DIR + '**/*.' + css, recursive=True):
            output_csv( css )

        # join_xls()

        subprocess.run(['echo', '正常に完了しました。'])

    except FileExistsError:
        subprocess.run(['echo', 'リストの抽出に失敗しました。'])
        pass
else:
    subprocess.run(['echo', REPOSITORY_DIR + 'ディレクトリが存在しません。mkdirでディレクトリを作成してください'])
    sys.exit()
