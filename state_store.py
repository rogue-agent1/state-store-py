#!/usr/bin/env python3
"""Redux-like state store with reducers, middleware, and selectors."""
import sys, copy

class Store:
    def __init__(self,reducer,initial_state=None,middleware=None):
        self.reducer=reducer; self.state=initial_state or {}
        self.listeners=[]; self.middleware=middleware or []; self.history=[copy.deepcopy(self.state)]
    def get_state(self): return self.state
    def dispatch(self,action):
        for mw in self.middleware: action=mw(self,action)
        if action is None: return
        self.state=self.reducer(self.state,action)
        self.history.append(copy.deepcopy(self.state))
        for fn in self.listeners: fn(self.state)
    def subscribe(self,fn): self.listeners.append(fn)
    def undo(self):
        if len(self.history)>1: self.history.pop(); self.state=copy.deepcopy(self.history[-1])

def todos_reducer(state,action):
    state=dict(state); todos=list(state.get("todos",[]))
    if action["type"]=="ADD_TODO": todos.append({"text":action["text"],"done":False})
    elif action["type"]=="TOGGLE_TODO": todos[action["index"]]["done"]=not todos[action["index"]]["done"]
    elif action["type"]=="REMOVE_TODO": todos.pop(action["index"])
    state["todos"]=todos; return state

def logger_mw(store,action):
    print(f"  dispatch: {action['type']}"); return action

if __name__ == "__main__":
    store=Store(todos_reducer,{"todos":[]},middleware=[logger_mw])
    store.subscribe(lambda s:None)
    store.dispatch({"type":"ADD_TODO","text":"Build tools"})
    store.dispatch({"type":"ADD_TODO","text":"Push to GitHub"})
    store.dispatch({"type":"TOGGLE_TODO","index":0})
    for t in store.get_state()["todos"]: print(f"  [{'x' if t['done'] else ' '}] {t['text']}")
    store.undo()
    print("After undo:")
    for t in store.get_state()["todos"]: print(f"  [{'x' if t['done'] else ' '}] {t['text']}")
