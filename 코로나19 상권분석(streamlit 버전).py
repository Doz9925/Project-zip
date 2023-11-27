import pandas as pd
import numpy as np
import branca
import platform
import plotly.express as px
import streamlit as st
import geopandas
import requests
import folium
from folium import Choropleth
from folium.features import GeoJsonPopup, GeoJsonTooltip
from streamlit_folium import st_folium
from shapely.geometry import Polygon

df_2021 = pd.read_csv('C:\jupyter\소상공인시장진흥공단_상가(상권)정보_202109\소상공인시장진흥공단_상가(상권)정보_서울_202109.csv')
df_2023 = pd.read_csv('C:\jupyter\소상공인시장진흥공단_상가(상권)정보_202309\소상공인시장진흥공단_상가(상권)정보_서울_202309.csv')


view_columns = ['상호명', '지점명', '상권업종대분류명', '상권업종중분류명',
              '상권업종소분류명', '시도명', '시군구명',
              '행정동명', '법정동명', '지번주소', '도로명주소', '경도', '위도']

df_2021 = df_2021[view_columns]
df_2023 = df_2023[view_columns]




select_multi_species = st.sidebar.multiselect(
    '확인하고자 하는 시군구명을 선택해 주세요. 복수선택가능',
    ['강남구', '서초구', '송파구', '마포구', '영등포구', '강서구', '중구', '종로구', '관악구', '금천구',
       '강동구', '구로구', '광진구', '성동구', '동대문구', '은평구', '용산구', '성북구', '양천구', '중랑구',
       '노원구', '서대문구', '동작구', '강북구', '도봉구']

)


st.header('서울시 상권 분석', divider='rainbow')
st.subheader(":red[COVID 19] 상황과 그 이후(서울 전체)")

if select_multi_species == []:

    col1,col2 = st.columns([20,20])
    count_2021=pd.value_counts(df_2021['상권업종대분류명'].values)
    count_2023=pd.value_counts(df_2023['상권업종대분류명'].values)

    with col1 :
        st.subheader(':red[2021년] 상업분류')
        fig = px.bar(count_2021.sort_values(), orientation='h')
        fig.update_traces(marker_color='#FF0000')
        st.plotly_chart(fig, use_container_width=True)
    with col2 :
        st.subheader(':blue[2023년] 상업분류')
        fig = px.bar(count_2023.sort_values(), orientation='h')
        st.plotly_chart(fig, use_container_width=True)
else:
    goo_2021 = df_2021[df_2021['시군구명'].isin(select_multi_species)]
    goo_2023 = df_2023[df_2023['시군구명'].isin(select_multi_species)]



    goo_count_2021=pd.value_counts(goo_2021['상권업종대분류명'].values)
    goo_count_2023=pd.value_counts(goo_2023['상권업종대분류명'].values)

    name = ', '.join(select_multi_species)
    st.title(name)
    col3,col4 = st.columns([20,20])
    with col3 :
        st.subheader(':red[2021년] 상업분류')
        fig = px.bar(goo_count_2021.sort_values(), orientation='h')
        fig.update_traces(marker_color='#FF0000')
        st.plotly_chart(fig, use_container_width=True)
    with col4 :
        st.subheader(':blue[2023년] 상업분류')
        fig = px.bar(goo_count_2023.sort_values(), orientation='h')
        st.plotly_chart(fig, use_container_width=True)


    food_2021 = goo_2021[goo_2021['상권업종대분류명'] == '음식']
    food_2023 = goo_2023[goo_2023['상권업종대분류명'] == '음식']


    food_count_2021 = pd.value_counts(food_2021['상권업종중분류명'].values)
    food_count_2023 = pd.value_counts(food_2023['상권업종중분류명'].values)

    st.header(':blue[음식 상권] 비교')
    col5,col6 = st.columns([20,20])
    with col5 :
        st.subheader(':red[2021년]의 음식 상권 비율')

        data = food_count_2021.values
        labels = food_count_2021.index

        fig = px.pie(values=data, names=labels)
        st.plotly_chart(fig, use_container_width=True)


    with col6 :
        st.subheader(':blue[2023년]의 음식 상권 비율')
        data = food_count_2023.values
        labels = food_count_2023.index

        fig = px.pie(values=data, names=labels)


        st.plotly_chart(fig, use_container_width=True)

    st.header(':blue[한식] 비교')
    col7,col8 = st.columns([20,20])
    with col7 :
        st.subheader(':red[2021년]의 한식분포')

        food_kor_2021=food_2021[food_2021['상권업종중분류명']=='한식'][['위도','경도']]
        food_kor_2021.columns=['lat','lon']

        st.map(food_kor_2021,
               latitude='lat',
               longitude='lon')

    with col8 :
        st.subheader(':blue[2023년]의 한식분포')
        
        food_kor_2023=food_2023[food_2023['상권업종중분류명']=='한식'][['위도','경도']]
        food_kor_2023.columns=['lat','lon']

        st.map(food_kor_2023,
               latitude='lat',
               longitude='lon',
               color='#ADD8E6')

    @st.cache_resource
    def get_seoul_data():

        df_2021 = pd.read_csv('C:\jupyter\소상공인시장진흥공단_상가(상권)정보_202109\소상공인시장진흥공단_상가(상권)정보_서울_202109.csv')
        df_2023 = pd.read_csv('C:\jupyter\소상공인시장진흥공단_상가(상권)정보_202309\소상공인시장진흥공단_상가(상권)정보_서울_202309.csv')


        view_columns = ['상호명', '지점명', '상권업종대분류명', '상권업종중분류명',
                '상권업종소분류명', '시도명', '시군구명',
                '행정동명', '법정동명', '지번주소', '도로명주소', '경도', '위도']

        df_2021 = df_2021[view_columns]
        df_2023 = df_2023[view_columns]

        map_2021 = df_2021[df_2021['상권업종대분류명'] == '음식']
        map_2021 = df_2021[df_2021['상권업종중분류명'] == '한식']

        map_2023 = df_2023[df_2023['상권업종대분류명'] == '음식']
        map_2023 = df_2023[df_2023['상권업종중분류명'] == '한식']

        map_count_2021 = pd.DataFrame(map_2021.groupby('시군구명')['상호명'].count())
        map_count_2023 = pd.DataFrame(map_2023.groupby('시군구명')['상호명'].count())

        seoul_geojson_url = 'https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo.json'
        seoul_geojson = requests.get(seoul_geojson_url).json()

        seoul_districts_coords = {}
        for feature in seoul_geojson['features']:
            name = feature['properties']['name']
            coordinates = feature['geometry']['coordinates'][0]
            seoul_districts_coords[name] = coordinates

        states =geopandas.GeoDataFrame(geometry=[Polygon(coords) for coords in seoul_districts_coords.values()],
                                index=seoul_districts_coords.keys())
        states.crs = 'EPSG:4326'
        states['count'] = map_count_2021
        states= states.reset_index()

        states1 =geopandas.GeoDataFrame(geometry=[Polygon(coords) for coords in seoul_districts_coords.values()],
                                index=seoul_districts_coords.keys())
        states1.crs = 'EPSG:4326'
        states1['count'] = map_count_2023
        states1= states1.reset_index()


        return states,states1
    
    col9,col10 = st.columns([20,20])
    df,df1 = get_seoul_data()
    m = folium.Map(location=[37.5665, 126.9780], zoom_start=10)  # 서울 중심으로 지도 설정
    m1 = folium.Map(location=[37.5665, 126.9780], zoom_start=10)


    colormap = branca.colormap.LinearColormap(
        vmin=df["count"].quantile(0.0),
        vmax=df["count"].quantile(1),
        colors=["red", "orange", "lightblue", "green", "darkgreen"],
        caption="State Level Median County Household Income (%)",
    )
    tooltip = GeoJsonTooltip(
        fields=["index", "count"],
        aliases=["State:", "매장수:  "],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )


    folium.GeoJson(
        df,
        style_function=lambda x: {
            "fillColor": colormap(x["properties"]["count"])
            if x["properties"]["count"] is not None
            else "transparent",
            "color": "black",
            "fillOpacity": 0.4,
        },
        tooltip=tooltip,
    ).add_to(m)

    colormap.add_to(m)

    return_on_hover = st.checkbox("Return on hover?", True)




    #####
    colormap = branca.colormap.LinearColormap(
        vmin=df1["count"].quantile(0.0),
        vmax=df1["count"].quantile(1),
        colors=["red", "orange", "lightblue", "green", "darkgreen"],
        caption="State Level Median County Household Income (%)",
    )
    tooltip = GeoJsonTooltip(
        fields=["index", "count"],
        aliases=["State:", "매장수:  "],
        localize=True,
        sticky=False,
        labels=True,
        style="""
            background-color: #F0EFEF;
            border: 2px solid black;
            border-radius: 3px;
            box-shadow: 3px;
        """,
        max_width=800,
    )


    folium.GeoJson(
        df1,
        style_function=lambda x: {
            "fillColor": colormap(x["properties"]["count"])
            if x["properties"]["count"] is not None
            else "transparent",
            "color": "black",
            "fillOpacity": 0.4,
        },
        tooltip=tooltip,
    ).add_to(m1)

    colormap.add_to(m1)

    with col9 :
        st.subheader(':red[2021년]서울시 한식분포')
        output = st_folium(m, width=550, height=500, return_on_hover=return_on_hover)
    with col10 :
        st.subheader(':blue[2023년]서울시 한식분포')
        output = st_folium(m1, width=550, height=500)
