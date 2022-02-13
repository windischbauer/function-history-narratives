from flask_graphql import GraphQLView
import config
import query

app = config.connex_app

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=query.schema,
        graphiql=True
    )
)


# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
