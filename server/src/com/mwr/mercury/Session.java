// License: Refer to the README in the root directory

package com.mwr.mercury;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;

import com.google.protobuf.ByteString;
import com.mwr.mercury.Message.Request;
import com.mwr.mercury.Message.Request.Builder;
import com.mwr.mercury.Message.Response;

import android.content.Context;
import android.util.Base64;
import android.util.Log;

public class Session
{
	private BufferedBracketReader input;
	private PrintWriter output;
	private Socket clientSocket;  
	public boolean connected;
	public Context applicationContext;

	//Assign session information
	Session(Socket client, Context ctx)
	{
		clientSocket = client;
		applicationContext = ctx;
		connected = true;

		try
		{
			//input = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()), 8192);		
			input = new BufferedBracketReader(new InputStreamReader(clientSocket.getInputStream()));
			output = new PrintWriter(clientSocket.getOutputStream(), true);
		}
		catch (Exception e) {}
		
		Log.e("mercury", "New session from " + clientSocket.getInetAddress().toString());
	}
	
	//Read from session - return contents
	public Request receive()
	{
		try
		{
			//Wait until ready
			//while (!input.ready());
			
			//Read from socket
			//String content = input.readLine();
			//String content = readTransmission(input);
			Request content = readTransmission(input);
					
			//Maintain whether connection is still connected or not
			if (content == null)
				connected = false;
			else
				connected = true;
			
			return content;
		}
		catch (IOException e)
		{
			connected = false;
			return null;
		}
	}
	
	private Request readTransmission(BufferedBracketReader in) throws IOException
	{
		//String out = "";
		//StringBuilder sb = new StringBuilder(512);
		//int cur = in.read();
		//while(cur == '\n' || cur  == '\r' || cur == ' ') cur = in.read();
		String out = "";
		//in.skipWs();
		DataInputStream dataInput = new DataInputStream(clientSocket.getInputStream());
		while(true) {
			//Log.d("RECV", "before");
            //read version
			dataInput.readShort();
            //read message type
			dataInput.readShort();
            //read message length
			dataInput.readInt();
			String r = "";
			String response = "";
			while ((r = dataInput.readLine()) != null) {
				response += r;
				if (response.endsWith("\n"));
					break;
			}
//			String r = in.readChunk();
			//Log.d("RECV", "after");
			try
			{
				byte[] buffer = Base64.decode(response, Base64.DEFAULT);
				Request request = Request.parseFrom(buffer);
				return request;
			}
			catch (Exception e)
			{
				if(r!=null) {
					//Log.d("RECV", r);
					out += r;
					if(out.endsWith("</transmission>")) {
						ArrayList<RequestWrapper> parsedCommands = new XML(out).getCommands();
						Request request = Request.getDefaultInstance();
						Builder builder = request.toBuilder();
						for (RequestWrapper requestWrapper : parsedCommands)
						{
							builder.setSection(requestWrapper.section);
							builder.setFunction(requestWrapper.function);
						}
						
						return builder.build();
					}
				}
			}
			
			
			/*
			sb.append((char)cur);
			 
			if (cur == (char)'>') {
				String out = sb.toString();
				if(out.endsWith("</transmission>"))
					return out;
			}
			cur = in.read();
			*/
		}
	}

	//Write to session - return success
	public boolean send(String data, boolean base64, short type)
	{
		try
		{
			DataOutputStream dataOutput = new DataOutputStream(clientSocket.getOutputStream());
			dataOutput.writeShort(Common.version);
			dataOutput.writeShort(type);
			dataOutput.writeInt(data.getBytes().length);
			dataOutput.write(data.getBytes());
		}
		catch (IOException e)
		{
			// TODO Auto-generated catch block
			e.printStackTrace();
			return false;
		}
		
		return true;

	}
		
	// Send a full transmission without worrying about structure
	// Should only be used for small responses < 50KB
	public void newSendFullTransmission(String response, String error)
	{		
		Response resp = Response.getDefaultInstance();
		Response.Builder builder = resp.toBuilder();
		ByteString bsResp = ByteString.copyFrom(response.getBytes());
		builder.setData(bsResp);
		if (error == null)
			builder.setError(ByteString.copyFrom("Null error given".getBytes()));
		else if (error.length() > 0)
			builder.setError(ByteString.copyFrom(error.getBytes()));
		resp = builder.build();
		
		send(Base64.encodeToString(resp.toByteArray(), Base64.DEFAULT), false, Common.COMMAND_REPLY);
	}
  
  
}
