def model_to_dict(model):

    if model is None:
        return None

    return {

        column.name: getattr(
            model,
            column.name
        )

        for column in model.__table__.columns

    }