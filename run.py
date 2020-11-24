

from app import app



if __name__=="__main__":
    app.run(debug=True)

# def errorhandler(e):
#     """Handle error"""
#     if not isinstance(e, HTTPException):
#         e = InternalServerError()
#     return apology(e.name, e.code)


# Listen for errors
# for code in default_exceptions:
#     app.errorhandler(code)(errorhandler) 
# coba ajaaa hehehe