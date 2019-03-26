import pynvim

from .qalc import process, qalc_exrates


@pynvim.plugin
class QalcPlugin:
    def __init__(self, nvim):
        self.nvim = nvim
        qalc_exrates()

    @pynvim.autocmd("BufEnter,TextChanged,TextChangedI", pattern="*.qalc")
    def on_trigger(self):
        buffer = self.nvim.current.buffer
        buf_id = buffer.number
        outs = dict(process(buffer))
        for i, _ in enumerate(buffer):
            out = outs.get(i, None)
            self.nvim.call(
                "nvim_buf_set_virtual_text",
                buf_id,
                10,
                i,
                [[out, "Error"]] if out is not None else [],
                {},
            )
