import streamlit as st

def page2():
    st.markdown("You can add core metrics here.")

def page3():
    st.markdown("Here's a third page. This one throws an error which is caught in the main script.")
    raise TypeError("This page has the wrong type")

def north_star():
    st.info("**Install Streamlit 1.36** to give it a try! 👈", icon="🎮")

    st.markdown("""
    Using the new API, when you do `streamlit run streamlit_app.py`, the contents of streamlit_app.py will automatically run before every page instead of defining the home page. Any common code can go here.

    - **Dynamic navigation API:** A new API called `st.navigation()` with `st.Page()` to programmatically define the available pages of your app. This means the available and displayed pages can change in a given session / rerun!
    - **Write common code once:** Besides defining your pages / nav, you can also add any common session setup code, authorization check, page_config, styles, etc only once in this file.
    - **Native logos and icons:** use `st.logo()` to add an app logo at the top left, add text headings between page groups in the native navigation, and (limited) support for Material icons in addition to emojis.

    Let us know what you think! Share bugs, public apps examples and what use-cases you build in the
    [Streamlit forum post](https://discuss.streamlit.io/t/coming-soon-multi-page-apps-improved-api-and-new-navigation-ui-features/65679).
                
    The navigation for this app is copied below. **View the [full source code here](https://github.com/streamlit/release-demos/blob/master/previews/mpa-v2/streamlit_app.py).**
    """)

    st.code("""
            pg = st.navigation({
                "Overview": [
                    # Load pages from functions
                    st.Page(north_star, title="Home", default=True, icon=":material/home:"),
                    st.Page(north_star, title="North Star", icon=":material/star_border:"),
                    ],
                "Metrics": [
                    st.Page(page2, title="Core Metrics", icon=":material/hourglass_top:"),
                    # You can also load pages from files, as usual
                    st.Page("movies.py", title="Movie Explorer", icon=":material/movie_filter:"),
                    st.Page(page3, title="App statuses over time", icon=":material/access_time:"),
                    st.Page(page3, title="Cloud apps leaderboard", icon=":material/share:"),
                    ],
            })
            pg.run()
            """)


def page4():
    @st.experimental_dialog("Input")
    def get_input():
        st.session_state.input = st.text_input("Some input")
        if st.button("Submit"):
            st.rerun()

    if st.button("Add input"):
        get_input()

    if input := st.session_state.get("input"):
        st.write(f"Welcome, {input}")