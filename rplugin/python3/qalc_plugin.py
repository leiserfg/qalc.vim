import pynvim
from qalc import process


@pynvim.plugin
class QalcPlugin:
    def __init__(self, nvim):
        self.nvim = nvim
 
    @pynvim.autocmd('BufWritePost', pattern='*.calc')
    def on_bufenter(self, filename):
        for i, v in process(self.nvim.current.buffer):
            self.nvim.call('nvim_buf_set_virtual_text', self.nvim.current.buffer, 0, i, [[v, 'Error']], {})
