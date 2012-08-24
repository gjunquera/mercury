// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import com.google.protobuf.ByteString;
import com.mwr.mercury.*;
import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Message.Response;

import android.util.Base64;

public class Core
{
	//core.ping() - returns "pong"
	public static void ping(List<KVPair> argsArray, Session currentSession){
		currentSession.newSendFullTransmission("pong", "");
	}
	
	//core.version() - returns Mercury version
	public static void version(List<KVPair> argsArray, Session currentSession){
		String version = "";
		try
		{
			version = currentSession.applicationContext.getPackageManager().getPackageInfo(currentSession.applicationContext.getPackageName(), 0).versionName;
		}
		catch (Exception e) {}
		currentSession.newSendFullTransmission(version, "");
	}
	
	public static void fileSize(List<KVPair> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		
		try
		{
			File file = new File(path);
			
			//Send the size of the file
			if (file.exists())
				currentSession.newSendFullTransmission(String.valueOf(file.length()), Common.ERROR_OK);
			else
				currentSession.newSendFullTransmission("", "File does not exist");
		}
		catch (Exception e)
		{
			currentSession.newSendFullTransmission("", e.getMessage());
		}
	}
	
	public static void fileMD5(List<KVPair> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		
		try
		{
			//Send the number of bytes in the file
			currentSession.newSendFullTransmission(Common.md5SumFile(path), Common.ERROR_OK);
		}
		catch (Exception e)
		{
			currentSession.newSendFullTransmission("", e.getMessage());
		}
	}
	
	public static void download(List<KVPair> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		Integer offset = Integer.parseInt(Common.getParamString(argsArray, "offset"));
		
		File file = new File(path);
		InputStream in = null;
		
		int buffSize = 50 * 1024; //50KB
		
		Response.Builder responseBuilder = Response.newBuilder();
		try
		{
			in = new BufferedInputStream(new FileInputStream(file));
			
			byte[] buffer = new byte[buffSize];
			
			for (int i = 0; i < offset; i++)
				in.read();
			
			int bytesRead = in.read(buffer, 0, buffSize);
			
			byte[] responseData = new byte[bytesRead];
			System.arraycopy(buffer, 0, responseData, 0, bytesRead);
			responseBuilder.setData(ByteString.copyFrom(responseData));
			responseBuilder.setError(ByteString.copyFrom(Common.ERROR_OK.getBytes()));
//			currentSession.send(new String(Base64.encode(buffer, 0, bytesRead, Base64.DEFAULT)) + "\n", false);
		
		}
		catch (Exception e)
		{
			responseBuilder.setError(ByteString.copyFrom(e.getMessage().getBytes()));
		}
		finally
		{
			//Close file
			if (in != null)
			{
				try
				{
					in.close(); 
				}
				catch (Exception e) {}
			}
		     
			currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
		}
	}
	
	public static void upload(List<KVPair> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		byte[] data = Common.getParam(argsArray, "data");
		
		File file = new File(path);
		BufferedOutputStream out = null;
		
		try
		{
			out = new BufferedOutputStream(new FileOutputStream(file,true)); 
			out.write(data);
			
			currentSession.newSendFullTransmission("", Common.ERROR_OK);
		
		}
		catch (Exception e)
		{
			currentSession.newSendFullTransmission("", e.getMessage());
		}
		finally
		{
			//Close file
			if (out != null)
			{
				try
				{
					out.close(); 
				}
				catch (Exception e) {}
			}
		}
	}
	
	public static void strings(List<KVPair> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		
		ArrayList<String> lines = Common.strings(path);
		Iterator<String> it = lines.iterator();
		
		Response.Builder responseBuilder = Response.newBuilder();		
		while (it.hasNext()) 
			responseBuilder.addStructuredData(Common.createKVPair("string", it.next()));

		currentSession.send(Base64.encodeToString(responseBuilder.build().toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}
	
	public static void unzip(List<KVPair> argsArray, Session currentSession){
		//Get path from arguments
		String filename = Common.getParamString(argsArray, "filename");
		String path = Common.getParamString(argsArray, "path");
		String destination = Common.getParamString(argsArray, "destination");
		
		//Unzip file
		boolean success = Common.unzipFile(filename, path, destination);
		
		if (success)
			currentSession.newSendFullTransmission("", Common.ERROR_OK);
		else
			currentSession.newSendFullTransmission("", "Unzip failed");
	}
	
	public static void delete(List<KVPair> argsArray, Session currentSession){
		//Get path from arguments
		String path = Common.getParamString(argsArray, "path");
		
		try
		{
			if (new File(path).delete())
				currentSession.newSendFullTransmission("", Common.ERROR_OK);
			else
				currentSession.newSendFullTransmission("", "Could not delete");
		}
		catch (Exception e)
		{
			currentSession.newSendFullTransmission("", e.getMessage());
		}
	}

}
