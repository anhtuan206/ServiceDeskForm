from application import create_app

app = create_app()

# Chạy ứng dụng ở mode debug của Flask
# if __name__ == '__main__':
#     app.run(debug=True,host='0.0.0.0',port=51806)


# Chạy ứng dụng ở mode ASGI
# from asgiref.wsgi import WsgiToAsgi
# asgi_app = WsgiToAsgi(app)
#hypercorn.exe app:app -b 0.0.0.0:51801 --debug --reload