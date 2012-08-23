// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import com.mwr.mercury.ArgumentWrapper;
import com.mwr.mercury.Common;
import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Session;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.List;

public class Shell
{
	public static void executeSingleCommand(List<KVPair> argsArray,
			Session currentSession)
	{
		// Get all the parameters
		String args = Common.getParamString2(argsArray, "args");

		String returnValue = "";

		// Execute a Linux command and get result
		try
		{

			// Default working directory
			File workDir = new File("/");
			String[] env = null;

			// Executes the process using sh -c command (so that piping features
			// etc. are present)
			Process proc = Runtime.getRuntime().exec(new String[]
			{ "sh", "-c", args }, env, workDir);

			// Wait for process to finish
			try
			{
				proc.waitFor();
			}
			catch (InterruptedException e)
			{
			}

			// Read output and error streams
			BufferedReader reader = new BufferedReader(new InputStreamReader(
					proc.getInputStream()));
			BufferedReader errorreader = new BufferedReader(
					new InputStreamReader(proc.getErrorStream()));

			String line;

			// Display output and error streams
			while ((line = errorreader.readLine()) != null)
				returnValue += line + "\n";

			while ((line = reader.readLine()) != null)
				returnValue += line + "\n";

		}
		catch (Exception e)
		{
			currentSession.newSendFullTransmission(e.getMessage(), "");
		}

		currentSession.newSendFullTransmission(returnValue.trim(), Common.ERROR_OK);

		return;
	}

	public static void newMercuryShell(List<KVPair> argsArray,
			Session currentSession)
	{
		Common.mercuryShell = new com.mwr.mercury.Shell();
		currentSession.newSendFullTransmission("", Common.ERROR_OK);
	}

	public static void executeMercuryShell(List<KVPair> argsArray,
			Session currentSession)
	{
		//Get all the parameters
		String args = Common.getParamString2(argsArray, "args");
		
		if (Common.mercuryShell.write(args))
			currentSession.newSendFullTransmission("", Common.ERROR_OK);
		else
			currentSession.newSendFullTransmission("", Common.ERROR_UNKNOWN);
	}

	public static void readMercuryShell(List<KVPair> argsArray,
			Session currentSession)
	{
		currentSession.newSendFullTransmission(Common.mercuryShell.read(), Common.ERROR_OK);
	}
}
