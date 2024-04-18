This is an example of a "custom" probe-agent. It does not use BaseProbeAgentActivator but rather creates its own.
BaseProbeAgentActivator is intended to help keep everything as simple as possible for the end user.
This example shows how to customize many properties not possible with the BaseProbeAgentActivator.
For example, you can provide your own means to configure your probes etc.

NOTE: It uses the current client(SAC) interface to hack an interface for creating probes on the fly, which results in
creating an extra "probe" that has no meaning from measurement point of view. However, this is perhaps best taken as
just an example of customization and ignoring any idea of "real" application of such functionality at this point.

NOTE2: You need to provide ALL of the following to register a probe/bm: target type, target name, bmclass, bm name.
If any of these are missing, the probe will fail to register.

Details:
CustomCore.java = a class that takes care of sharing resources across "Probe" interface implementations.
CoreConfigurationHandler.java = the "fake" probe that allows creation of other probes.
CustomProbeActivator.java = The OSGI bundle activator that starts it up and glues it to the generic probe-agent.
CustomProbeFacade.java = One of these is created for each "Probe" that is created on the fly.

Usage instructions:
To install, copy the ssh-agent.jar over the same file in the SSH probe-agent distribution bundles dir.

When you have everything running, you should see a probe named "CustomTarget1" on the server-agent web-ui.
Go to "Availability" tab. Note the "Probe ID" for this probe.
Now go to "Probe Parameters" tab. Put the value you noted for "Probe ID" in the field "Probe ID".
Hit the "Get Parameters" button.
Insert into field "Parameter Name" the value "add".
Insert into field "Parameter Value" the following properties "ttype/tname/bmclass/bmname/pname".
Replace the values with anything you like as long as there is something:
-ttype = target type
-tname = target name
-bmclass = bm class
-bmname = bm name
-pname = probe name
Hit the "Set Parameter" button.
Go to Availability tab again.
You should now see your new probe listed under "Available Probes". Note again your "Probe ID".
Go to "Probe Parameters" tab again. Insert the id into the field as before. Get parameters.
Now set the parameters with the names in the list. These are
login = username for login
password = password for login
script = what script should be executed, e.g. "echo here is the result"
target = the ip/name of the host where to run the script

once you have all these set, you should go to the "History" tab and if all went perfectly it is now showing results
from your new probe/bm you just deployed.


