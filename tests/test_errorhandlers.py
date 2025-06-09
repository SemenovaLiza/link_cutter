def test_404(client):
    got = client.get('/enexpected')
    assert got.status_code == 404, (
        'When accessing a non-existent page, return the status code `404`'
    )
    assert (
        'If you entered the URL manually please check your spelling and try again.'  # noqa
        not in got.data.decode('utf-8')
    ), (
        'Add error-handlers for access to non-existent pages.'
        'Use 404.html template'
    )
