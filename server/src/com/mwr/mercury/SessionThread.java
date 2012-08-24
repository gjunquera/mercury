// License: Refer to the README in the root directory

package com.mwr.mercury;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Message.Request;
import com.mwr.mercury.reflect.ReflectParser;

import android.util.Log;

class SessionThread extends Thread
{
	Session currentSession;
	ReflectParser parser;
  
	//Assign session variables
	SessionThread(Session session)
	{
		currentSession = session;
		parser = new ReflectParser(session);
	}
	
	@Override
	protected void finalize() throws Throwable
	{
		super.finalize();
		Log.e("mercury", "Closing thread");
	}
  
	//This thread receives commands from the client and handles command
	public void run()
	{
		while (currentSession.connected)
		{
			//String received = currentSession.receive();
			Request received = currentSession.receive();
			//Pass off command to be handled
			if (received != null) //Check that it is not null
				//if(!parser.parse(received))
					handleCommand(received);
		}
		Log.e("mercury", "Exiting thread");
	}
  
  
	//Redirect commands to be handled by different functions
		public void handleCommand(Request request)
		{
			//Create an array of commands from xml request received
			//ArrayList<RequestWrapper> parsedCommands = new XML(xmlInput).getCommands();
			//Command has been found on server
			boolean found = false;
		
			//Iterate through received commands
//			for (int i = 0; i < parsedCommands.size(); i++)
//			{
				try
				{
					// Do some hard work to get the class name
					StringBuilder className = new StringBuilder(
							currentSession.applicationContext.getPackageName() + ".commands.");
					String section = request.getSection();
					className.append(Character.toUpperCase(section.charAt(0)))
					.append(section.substring(1).toLowerCase());
					
					// Search for the class that represents a section
					Class<?> c = Class.forName(className.toString());
					if (null != c)
					{
						Method[] methods = c.getMethods();
						for (Method method : methods)
						{
							// If method name equals function name, execute the command
							if (method.getName().equalsIgnoreCase(request.getFunction())
									&& null != method)
							{
								found = true;
								List<KVPair> reqArgs = request.getArgsList();
								method.invoke(null, reqArgs, currentSession);
								break;
							}
						}
					}
				}
				catch (Exception e)
				{
					currentSession.newSendFullTransmission("", "Command not found on Mercury server");
				}
//			}
			
			//Default case if command not found
			if (!found)
				currentSession.newSendFullTransmission("", "Command not found on Mercury server");
	  }
  
  
}
