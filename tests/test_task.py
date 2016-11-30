# -*- coding: utf-8 -*-
import json
from app.database import model
from app.tasks.tasks import do_webhook_shell
from . import WEBHOOKDATA


def test_do_webhook_shell(create_server, create_webhook, sql):
    server = create_server()
    webhook = create_webhook(server_id=server['id'])
    data = WEBHOOKDATA['github']
    history = model.History(
        status='1',
        webhook_id=webhook['id'],
        data=json.dumps(data)
    )
    sql.add(history)
    sql.commit()
    history_id = history.id
    text = 'select * from history where id=:id'
    result = sql.execute(text, {'id': history_id}).fetchone()
    assert result.status == '1'
    do_webhook_shell.apply(args=(webhook['id'], history_id, data)).get()
    result = sql.execute(text, {'id': history_id}).fetchone()
    assert result.status == '5'
