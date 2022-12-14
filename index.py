import streamlit as st
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

st.set_page_config(page_title="SOjaアンケート")

def post_answer(dic_answers):
    db_url = st.secrets["db_url"]
    with MongoClient(db_url, server_api=ServerApi('1')) as client:
        db = client["so-survey"]
        collection = db["answer"]
        collection.insert_one(dic_answers)
        
dic_answers = {"userid":"",
               "skill":"",
               "goodness":"",
               "wanted":"",
               "benice":"",
               "moderators":"",
               "food":"",
               "events":"",
               "others":"",}

st.title("スタック・オーバーフロー(SOja)のアンケート")
st.header("アンケート")
form = st.form("main-form")
dic_answers["userid"] = form.text_input("1.ユーザID", value=dic_answers["userid"], placeholder="匿名可。ja.stackoverflow.comのユーザID(数値)")
#form.text_area("SOに投稿したきっかけ", placeholder="あああああ")
dic_answers["skill"] = form.text_input("2.好きな/得意なタグ", placeholder="python javascript アルゴリズム")
dic_answers["goodness"] = form.text_area("3.SOjaの良いところ", placeholder="回答者に優しい人が多い気がする")
dic_answers["wanted"] = form.text_area("4.SOjaへの要望", placeholder="障害時の状況が日本語のチャットやTwitterで分かると嬉しい", help="思いつかない場合は優しく空欄にしてあげてね")
dic_answers["benice"] = form.text_area("5.Be niceであるために心がけてること", placeholder="積極的に新しい参加者のレビューをする")
dic_answers["moderators"] = form.text_area("6.モデレータさんへ激励の言葉", placeholder="いつもありがとう", help="普段は言う機会のないありがとうを書こう！")
dic_answers["food"] = form.text_area("7.コーディング時の食べ物や飲み物", placeholder="本気出すときはエナドリ。普段は猫吸い", help="")
dic_answers["events"] = form.text_area("8.SOjaのイベントへの意見", placeholder="あのイベントもしたい、このイベントもしたい。もっともっとイベントしたい！")
dic_answers["others"] = form.text_area("9.その他なんでも", placeholder="正式版おめでとう。愛してるぜ！")
form.write("プライバシーポリシー")
form.caption("このアンケートの結果は匿名で開示され、集計や発表資料の作成に使用されることがあります。")
form.caption("ユーザIDは不特定多数に開示されません。  \nただしユーザIDを含むアンケートの全回答はスタック・オーバーフローのスタッフおよびスタッフが認める特定のメンバーに共有されます。")
form.caption("このサイト利用および回答により直接的、間接的にいかなる損害を被った場合であっても、サイト主催者は一切の責任を負わず、一切の損害を補償しません。")
c = form.checkbox("プライバシーポリシーに同意する")
submit = form.form_submit_button('投稿')

if submit:
    if not c:
        st.error("プライバシーポリシーに同意してください。")
    elif f"{dic_answers['goodness']}{dic_answers['wanted']}{dic_answers['benice']}{dic_answers['moderators']}{dic_answers['events']}{dic_answers['others']}".strip() == "":
        st.error("一つ以上のアンケート欄にご記入をお願いいたします。")
    else:
        post_answer(dic_answers)
        st.balloons()
        st.write("ご協力ありがとうございました。")
