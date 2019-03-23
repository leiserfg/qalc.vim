import pynvim

from .qalc import process
from .util import debounce


@pynvim.plugin
class QalcPlugin:
    def __init__(self, nvim):
        self.nvim = nvim

    @pynvim.autocmd("BufNewFile,BufRead,TextChanged,TextChangedI", pattern="*.qalc")
    def on_bufenter(self):
        lines = list(self.nvim.current.buffer)
        buf_id = self.nvim.current.buffer.number
        self.nvim.async_call(lambda: self.asyn_process(lines, buf_id))

    @debounce(0.2)
    def asyn_process(self, lines, buf_id):
        for i, v in process(lines):
            self.nvim.async_call(
                lambda: self.nvim.call(
                    "nvim_buf_set_virtual_text", buf_id, 0, i, [[v, "Error"]], {}
                )
            )
