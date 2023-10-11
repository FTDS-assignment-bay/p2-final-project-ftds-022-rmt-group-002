import streamlit as st
import pandas as pd
import numpy as np

from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool, PanTool, ResetTool, WheelZoomTool
from bokeh.models.formatters import NumeralTickFormatter

# Simpan kode Bokeh Anda ke dalam fungsi
def create_bokeh_plot(df):
    # Mengonversi kolom 'datetime' ke tipe datetime
    df['datetime'] = pd.to_datetime(df['datetime'])

    # Mengatur kolom 'datetime' sebagai indeks DataFrame
    df.set_index('datetime', inplace=True)

    # Mengelompokkan data berdasarkan tahun dan menghitung harga rata-rata tahunan
    yearly_avg_price = df.resample('Y').agg({'price': 'mean'})

    # Menghitung perubahan harga emas
    df['price_change'] = df['price'].diff()

    # Membuat sumber data Bokeh
    source = ColumnDataSource(df)

    # Membuat plot interaktif dengan Bokeh
    p = figure(x_axis_type="datetime", title='Harga Emas (2010-2023)', sizing_mode="scale_width", width=800, height=500)  # Mengatur lebar plot
    p.line('datetime', 'price', source=source, line_width=2, legend_label='Harga Emas', line_color='blue')

    # Menambahkan tooltip interaktif
    hover = HoverTool()
    hover.tooltips = [("Tanggal", "@datetime{%F}"), ("Harga Emas", "@price{0,0}")]  # Format angka
    hover.formatters = {"@datetime": "datetime"}
    p.add_tools(hover)

    # Menambahkan alat zoom dan geser
    p.add_tools(PanTool(), ResetTool(), WheelZoomTool())

    # Mengatur label sumbu x dan y
    p.xaxis.axis_label = "Tahun"
    p.yaxis.axis_label = "Harga Emas"

    # Mengatur format angka pada sumbu y
    p.yaxis.formatter = NumeralTickFormatter(format='0a')

    return p

def run():
    # Load Data
    data = pd.read_csv('historik_antam.csv')

    # Aplikasi Streamlit
    st.title("Aplikasi Harga Emas")

    # Tampilkan plot Bokeh menggunakan st.bokeh_chart
    st.write('Something Something Grafik Harga Emas')
    bokeh_plot = create_bokeh_plot(data)
    st.bokeh_chart(bokeh_plot, use_container_width=True)

    st.write('Penjelasan EDA')

# Jangan lupa untuk menjalankan aplikasi dengan perintah
# streamlit run app.py

if __name__ == '__main__':
    run()