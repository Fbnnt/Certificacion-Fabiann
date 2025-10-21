from base import create_app


app = create_app()


if __name__ == "__main__":
    # Disable the auto-reloader to avoid confusing duplicate startup messages
    app.run(host='127.0.0.1', port=5038, debug=True, use_reloader=False)