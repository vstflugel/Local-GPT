import curses
import time
from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ChatUI:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.agent = Agent(model=Groq(id="deepseek-r1-distill-qwen-32b"))
        self.init_ui()
        
    def init_ui(self):
        curses.curs_set(1)  # Visible cursor
        self.stdscr.nodelay(0)
        self.stdscr.timeout(100)
        self.init_colors()
        self.resize_handler()

    def init_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # User input
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)  # AI response
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Header

    def resize_handler(self):
        self.rows, self.cols = self.stdscr.getmaxyx()
        self.header_height = 3
        self.input_height = 3
        self.chat_height = self.rows - self.header_height - self.input_height
        
        # Create windows
        self.header_win = curses.newwin(self.header_height, self.cols, 0, 0)
        self.chat_win = curses.newwin(self.chat_height, self.cols, self.header_height, 0)
        self.input_win = curses.newwin(self.input_height, self.cols, self.rows - self.input_height, 0)

    def draw_header(self):
        self.header_win.clear()
        title = " Groq Chat Assistant "
        self.header_win.addstr(1, (self.cols - len(title))//2, title, curses.color_pair(3))
        self.header_win.refresh()

    def draw_chat(self, messages):
        self.chat_win.clear()
        max_lines = self.chat_height - 2
        start_idx = max(0, len(messages) - max_lines)
        
        for i, (role, text) in enumerate(messages[start_idx:]):
            y = i + 1
            if y >= self.chat_height - 1:
                break
            color = curses.color_pair(1) if role == "user" else curses.color_pair(2)
            self.chat_win.addstr(y, 1, f"{role}: {text}", color)
        self.chat_win.refresh()

    def get_input(self):
        self.input_win.clear()
        self.input_win.addstr(1, 1, "You: ", curses.color_pair(1))
        self.input_win.refresh()
        curses.echo()
        input_str = self.input_win.getstr(1, 6, self.cols - 7).decode('utf-8')
        curses.noecho()
        return input_str.strip()

    def run(self):
        messages = []
        self.draw_header()
        
        while True:
            self.resize_handler()
            self.draw_header()
            self.draw_chat(messages)
            
            try:
                user_input = self.get_input()
                if user_input.lower() == 'exit':
                    break
                
                if user_input:
                    messages.append(("user", user_input))
                    response = self.agent.print_response(user_input)
                    messages.append(("AI", response))
                    
            except curses.ERR:
                pass
            except KeyboardInterrupt:
                break

def main(stdscr):
    chat_ui = ChatUI(stdscr)
    chat_ui.run()

if __name__ == "__main__":
    curses.wrapper(main)
