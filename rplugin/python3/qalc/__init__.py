import pynvim
from .qalc import process
from .util import throttle

@pynvim.plugin
class QalcPlugin:
    def __init__(self, nvim):
        self.nvim = nvim
 
    @pynvim.autocmd('BufNewFile,BufRead,TextChanged,TextChangedI', pattern='*.qalc')
    @throttle(0.3)
    def on_bufenter(self):
        for i, v in process(self.nvim.current.buffer):
            self.nvim.call('nvim_buf_set_virtual_text', self.nvim.current.buffer, 0, i, [[v, 'Error']], {})
