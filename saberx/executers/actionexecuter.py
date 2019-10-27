from saberx.sabercore.triggers.filetrigger import FileTrigger
from saberx.sabercore.triggers.processtrigger import ProcessTrigger
from saberx.sabercore.triggers.cputrigger import CPUTrigger
from saberx.sabercore.triggers.memorytrigger import MemoryTrigger
from saberx.sabercore.triggers.tcptrigger import TCPTrigger
from saberx.sabercore.shellexecutor import ShellExecutor

class ActionExecuter(object):

    @staticmethod
    def execute_action(**kwargs):

        '''
        The layout of a action will be as follows:

        action_1:
	        action_name: string
	        trigger:
		        type: TCP_TRIGGER
		        check: tcp_connect | tcp_fail
		        host: host_name
		        port: port
		        negate: true | false
		        attemp: number
		        threshold: number
		        ssl: true | false
	        execute:
	        - command1
	        - command2
        '''
        action = kwargs.get("action")
        thread_lock = kwargs.get("thread_lock")

        if not ActionExecuter.sanitize(action):
            return False

        trigger_map = {
            "FILE_TRIGGER": FileTrigger,
            "PROCESS_TRIGGER": ProcessTrigger,
            "TCP_TRIGGER": TCPTrigger,
            "CPU_TRIGGER": CPUTrigger,
            "MEMORY_TRIGGER": MemoryTrigger
        }

        action_name = action.get("action_name")
        trigger = action.get("trigger")
        execute = action.get("execute")

        triggerHandler = trigger_map.get(trigger.get("type"))(**trigger)
        triggered, error = triggerHandler.fire_trigger()

        if error:
            '''
                Log the error and return False. Consider the trgger as a failure.
            '''
            return False

        if triggered:
            shellExecuter = ShellExecutor(command_list=execute)
            with thread_lock:
                success = shellExecuter.execute_shell_list()
            return success

        return True

    @staticmethod
    def sanitize(action):
        return True
