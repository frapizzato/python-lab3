from telegram.ext import Updater,CommandHandler,MessageHandler,Filters
from telegram import ChatAction

list = []

def load_list(file):
    f = open(file,"r")
    tmp = f.readlines()
    for string in tmp:
        list.append(string.strip())
    f.close()

def update_file(file="task_list.txt"):
    f = open(file, "w")
    for task in list:
        f.write(task + "\n")
    f.close()

def start(bot,update):
    update.message.reply_text("Ciao Edoardo è un coglione!")

def echo_err(bot,update):
    bot.sendChatAction(update.message.chat_id,ChatAction.TYPING)
    update.message.reply_text("I'm sorry, can not do that!")

def showTasks(bot,update):
    bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)
    if not list:
        update.message.reply_text("Nothing to do here!")
    else:
        update.message.reply_text(sorted(list))

def newTask(bot,update, args):
    if not args:
        update.message.reply_text("Insert a task to add!")
    else:
        list.append(" ".join(args))
        bot.sendChatAction(update.message.chat_id,ChatAction.TYPING)
        update.message.reply_text("Task successfully added!")
        update_file()

def removeTask(bot,update,args):
    task = " ".join(args)
    for s in list:
        if s==task:
            list.remove(task)
            update.message.reply_text("The task was successfully deleted!")
            update_file()
            return
    update.message.reply_text("The task you specified is not in the list!")

def removeAllTasks(bot,update,args):
    remove = []
    sub_string = args[0]
    for task in list:
        if (sub_string in task):
            remove.append(task)
    if len(remove)>0:
        s = "The elements: "
        for l in remove:
            list.remove(l)
            s = s + "\"" + l + "\", "
        update.message.reply_text(s + " have been removed.")
        update_file()



def main():
    """
    This bot is a simple task manager
    """
    load_list("task_list.txt")

    """
    Here start the managing of the bot
    """
    #create the EventHandler
    updater = Updater("TOKEN")

    #get the dispacer to register handlers
    dp = updater.dispatcher

    #add handler for the start command
    dp.add_handler(CommandHandler("start",start))
    #add handler for "/showTasks
    dp.add_handler(CommandHandler("showTasks",showTasks))
    # add handler for "/newTask"
    dp.add_handler(CommandHandler("newTask", newTask, pass_args=True))
    # add handler for "/removeTask"
    dp.add_handler(CommandHandler("removeTask", removeTask, pass_args=True))
    # add handler for "/removeAllTasks"
    dp.add_handler(CommandHandler("removeAllTasks", removeAllTasks, pass_args=True))

    # on non-command textual messages - echo error message
    dp.add_handler(MessageHandler(Filters.text, echo_err))

    #start the bot
    updater.start_polling()
    #loop the bot
    updater.idle()

if __name__ == '__main__':
    main()

