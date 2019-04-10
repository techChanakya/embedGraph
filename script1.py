from flask import Flask, render_template

app=Flask(__name__)

@app.route('/plot/')
def plot():
    from pandas_datareader import data
    import datetime
    from bokeh.plotting import figure, show, output_file
    from bokeh.embed import components
    from bokeh.resources import CDN

    start=datetime.datetime(2015,11,1)
    end=datetime.datetime(2016,3,10)

    df=data.DataReader("GOOG","yahoo",start,end)
    df[["Open","High","Low","Close","Volume","Adj Close"]]

    def inc_dec(c, o):
        if c > o:
            return "Increase"
        elif c < o:
            return "Decrease"
        else:
            return "Equal"

    df["Status"]=[inc_dec(c,o) for c, o in zip(df.Close,df.Open)]
    df["Middle"]=(df.Close+df.Open)/2
    df["Height"]=abs(df.Close-df.Open)

    p=figure(x_axis_type='datetime',width=1000,height=300,sizing_mode='scale_width')
    p.title.text="Candlestick Chart"
    p.title.text_font_size={"value":"20pt"}
    p.title.align="center"
    #p.grid.grid_line_alpha=1

    hours_12=12*60*60*1000

    p.rect(df.index[df.Status=="Increase"],df.Middle[df.Status=="Increase"],
           hours_12, df.Height[df.Status=="Increase"],fill_color="green",line_color="black")
    p.rect(df.index[df.Status=="Decrease"],df.Middle[df.Status=="Decrease"],
           hours_12, df.Height[df.Status=="Decrease"],fill_color="red",line_color="black")
    p.segment(df.index,df.High,df.index,df.Low,color="black")

    script1, div1 = components(p)
    cdn_js=CDN.js_files[0]
    cdn_css=CDN.css_files[0]
    return render_template("plot.html", script1=script1, div1=div1, cdn_css=cdn_css, cdn_js=cdn_js)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about/')
def about():
    return render_template("about.html")

# if __name__=="__main__":
#    app.run(host='0.0.0.0', port=5000)
if __name__=="__main__":
    app.run(debug=True)
