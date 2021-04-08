from flask import Flask, redirect, url_for, request
from werkzeug.routing import BaseConverter  # 导入转换器基类

# 自定义正则转换器
class RegexConverter(BaseConverter):
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        # 将接受的第1个参数当作匹配规则进行保存
        self.regex = args[0]


app = Flask(__name__)
app.url_map.converters['re'] = RegexConverter


@app.route('/success/<name>')
def success(name):
    return "welcome %s" % name

@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == "POST":
        user = request.form['nm']
        return redirect(url_for('success',name = user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name = user))





if __name__ == '__main__':
    app.run(debug=True)