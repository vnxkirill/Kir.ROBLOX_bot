' GameCore AI — запуск run_bot.cmd в скрытом окне (без чёрной консоли).
Set shell = CreateObject("WScript.Shell")
shell.Run """" & CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName) & "\run_bot.cmd""", 0, False
