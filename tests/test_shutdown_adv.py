from mcai_agent import shutdown


def test_register_signal_handlers_idempotent():
    sh = shutdown.Shutdown()
    # just ensure it doesn't raise
    shutdown.register_signal_handlers(sh)
    shutdown.register_signal_handlers(sh)
    sh.request()
    assert sh.is_set()
