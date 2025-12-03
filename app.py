from pathlib import Path
import pandas as pd
import streamlit as st
from streamlit.components.v1 import html as st_html

st.set_page_config(page_title="Scrape Movies", layout="wide")

DATA_PATH = Path("movies.csv")


def load_data(path: Path) -> pd.DataFrame | None:
    if not path.exists():
        return None
    return pd.read_csv(path)


def load_html_page(page: int) -> str | None:
    path = Path(f"page{page}.html")
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8")


def scrape_and_reload():
    from scrape import main as scrape_main

    try:
        scrape_main()
    except Exception as exc:  # noqa: BLE001 - surface to UI
        st.error(f"抓取失敗: {exc}")
        return
    st.success("抓取完成，資料已更新。")
    st.rerun()


def render_summary(df: pd.DataFrame):
    cols = st.columns(3)
    cols[0].metric("電影數量", len(df))
    cols[1].metric("平均評分", f"{df['Score'].astype(float).mean():.2f}")
    unique_categories = set()
    for cats in df["Categories"].dropna():
        unique_categories.update(cat for cat in cats.split("|") if cat)
    cols[2].metric("類別數量", len(unique_categories))


def render_tables(df: pd.DataFrame):
    st.subheader("電影列表")
    st.dataframe(df, use_container_width=True)

    st.subheader("類別分佈")
    cat_count = {}
    for cats in df["Categories"].dropna():
        for cat in cats.split("|"):
            cat_count[cat] = cat_count.get(cat, 0) + 1
    cat_df = (
        pd.DataFrame([{"Category": k, "Count": v} for k, v in cat_count.items()])
        .sort_values("Count", ascending=False)
        .reset_index(drop=True)
    )
    st.dataframe(cat_df, use_container_width=True)


def render_html_preview():
    st.subheader("HTML 頁面預覽")
    col = st.columns([1, 4])[0]
    page = col.number_input("選擇頁碼", min_value=1, max_value=10, value=1, step=1)
    html_text = load_html_page(page)
    if html_text is None:
        st.info(f"找不到 page{page}.html，請先按「重新抓取資料」。")
        return
    st.caption(f"預覽: page{page}.html（來源 https://ssr1.scrape.center/page/{page}）")
    st_html(html_text, height=800, scrolling=True)


def main():
    st.title("Movie Scraper")
    st.write("顯示 scrape.py 抓取的結果，並可重新抓取。")

    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("重新抓取資料", use_container_width=True):
            with st.spinner("抓取中，請稍候..."):
                scrape_and_reload()
        st.caption("按下後會重新呼叫 scrape.py 並更新 movies.csv。")
        st.caption("HTML 會同步寫入 page1.html ~ page10.html。")

    df = load_data(DATA_PATH)
    if df is None:
        st.warning("找不到 movies.csv，請先點擊上方按鈕抓取資料。")
        return

    render_summary(df)
    render_tables(df)
    render_html_preview()


if __name__ == "__main__":
    main()
