// License: Refer to the README in the root directory

package com.mwr.mercury;

import java.io.BufferedInputStream;
import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.Serializable;
import java.math.BigInteger;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.security.MessageDigest;
import java.util.ArrayList;
import java.util.Enumeration;
import java.util.Iterator;
import java.util.List;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

import com.google.protobuf.ByteString;
import com.mwr.mercury.Message.KVPair;

import android.content.ComponentName;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.util.Log;

//An interface to use in CommandWrapper to better define Commands
interface Executor { public void execute(List<ArgumentWrapper> argsArray, Session currentSession); }

//A class to wrap commands and their implementations inside
class CommandWrapper
{
	public String section;
	public String function;
	public Executor executor;
	
	public CommandWrapper(String inputSection, String inputFunction, Executor inputExecutor)
	{
		section = inputSection;
		function = inputFunction;
		executor = inputExecutor;
	}
}

//A class to wrap requests that come in
class RequestWrapper
{
	public String section;
	public String function;
	public List<ArgumentWrapper> argsArray;
}

public class Common
{	
	public static final String ERROR_OK = "SUCCESS";
	public static final String ERROR_UNKNOWN = "ERROR";
	
	//Mercury persistent shell
	public static Shell mercuryShell = null;
	
	//Get all local IP addresses - needs INTERNET permission
	public static ArrayList<String> getLocalIpAddresses()
	{		
		
		ArrayList<String> ips = new ArrayList<String>();
		
	    try
	    {
	    	//Iterate over all network interfaces
	        for (Enumeration<NetworkInterface> en = NetworkInterface.getNetworkInterfaces(); en.hasMoreElements();)
	        {
	        	//Get next network interface
	            NetworkInterface intf = en.nextElement();
	            
	            //Iterate over all IP addresses
	            for (Enumeration<InetAddress> enumIpAddr = intf.getInetAddresses(); enumIpAddr.hasMoreElements();)
	            {
	            	//Get next IP address
	                InetAddress inetAddress = enumIpAddr.nextElement();
	                
	                //Add IP address if it is not a loopback address
	                if (!inetAddress.isLoopbackAddress())
	                	ips.add(inetAddress.getHostAddress().toString());
	                    
	            }
	        }
	        
	    }
	    catch (SocketException ex)
	    {
	        Log.e("getLocalIpAddress", ex.toString());
	    }
	    
	    return ips;
	}
	
	//Get md5Sum of file
	public static String md5SumFile(String path)
	{
		String md5 = "";
		
		try
		{
			MessageDigest digest = MessageDigest.getInstance("MD5");
			InputStream is = new FileInputStream(new File(path));				
			byte[] buffer = new byte[8192];
			int read = 0;
			try
			{
				while( (read = is.read(buffer)) > 0)
				{
					digest.update(buffer, 0, read);
				}	
				
				byte[] md5sum = digest.digest();
				BigInteger bigInt = new BigInteger(1, md5sum);
				md5 = bigInt.toString(16);
			}
			catch(IOException e)
			{
				throw new RuntimeException("Unable to process file for MD5", e);
			}
			finally
			{
				try
				{
					is.close();
				}
				catch(IOException e) {}
			}	
		}
		catch (Exception e) {}
		
		return md5;
	}
	
	//Get parameter from a List<ArgumentWrapper> in byte[] format
	//TODO remove this method
	public static byte[] getParam(List<ArgumentWrapper> argWrapper, String type)
	{
		
		for (int i = 0; i < argWrapper.size(); i++)
		{
			if (argWrapper.get(i).type.toUpperCase().equals(type.toUpperCase()))
				return argWrapper.get(i).value;
		}
		
		return null;
	}
	
	//Get parameter from a List<ArgumentWrapper> in byte[] format
	//TODO change this method name
	public static byte[] getParam2(List<KVPair> pairsArray, String key)
	{
		
		if (key == null || pairsArray == null) 
			return null;
		
		for (KVPair pair : pairsArray) 
		{
			String pairKey = pair.getKey();
			if (pairKey != null) 
				if (pairKey.equalsIgnoreCase(key))
					return pair.getValueList().get(0).toByteArray();
		}
		return null;
	}
	
	//Get parameter from a List<ArgumentWrapper> in String format
	//TODO remove this method
	public static String getParamString(List<ArgumentWrapper> argWrapper, String type)
	{
		byte[] param = getParam(argWrapper, type); 
		if (getParam(argWrapper, type) == null)
			return "";
		else return new String(param);
	}
	
	//TODO change this method name
	//Get parameter from a List<Args>
	public static String getParamString2(List<KVPair> pairsArray, String key) 
	{
		byte[] param = getParam2(pairsArray, key);
		if (param == null) 
			return "";
		else return new String(param);
	}

	//Get parameter from a List<ArgumentWrapper> in List<String> format
	//TODO remove this method
	public static List<String> getParamStringList(List<ArgumentWrapper> argWrapper, String type)
	{
		List<String> returnValues = new ArrayList<String>();
		
		for (int i = 0; i < argWrapper.size(); i++)
		{
			if (argWrapper.get(i).type.toUpperCase().equals(type.toUpperCase()))
				returnValues.add(new String(argWrapper.get(i).value));
		}
		
		return returnValues;
	}
	
	//Get parameter from a List<ArgumentWrapper> in List<String> format
	//TODO change this method name
	public static List<String> getParamStringList2(List<KVPair> pairsArray, String key)
	{
		List<String> returnValues = new ArrayList<String>();
		
		if (key == null || pairsArray == null) 
			return returnValues;
		
		for (int i = 0; i < pairsArray.size(); i++) 
		{
			KVPair pair = pairsArray.get(i);
			String pairKey = pair.getKey();
			if (pairKey != null) 
				if (pairKey.equalsIgnoreCase(key))
					for (int j = 0; j < pair.getValueList().size(); j++)
						returnValues.add(new String(pair.getValue(j).toByteArray()));
		}
		
		return returnValues;
	}

	
	//Convert a List to a contentvalues structure by splitting by =
	public static ContentValues listToContentValues(List<String> values, String type)
	{
		ContentValues contentvalues = new ContentValues();
	    
	    //Place values into contentvalue structure
	    for (int i = 0; i < values.size(); i++)
	    {
	    	String current = values.get(i);
	    	
	    	try
	    	{    	
		    	//Separate the value by = in order to get key:value
		    	Integer indexOfEquals = current.indexOf("=");
		    	String key = current.substring(0, indexOfEquals);
		    	String value = current.substring(indexOfEquals + 1);
		
		    	if (type.toUpperCase().equals("STRING"))
		    		contentvalues.put(key, value);
		    	
		    	if (type.toUpperCase().equals("BOOLEAN"))
		    		contentvalues.put(key, Boolean.valueOf(value));
	
		    	if (type.toUpperCase().equals("INTEGER"))
		    		contentvalues.put(key, new Integer(value));
		    	
		    	if (type.toUpperCase().equals("DOUBLE"))
		    		contentvalues.put(key, new Double(value));
		    	
		    	if (type.toUpperCase().equals("FLOAT"))
		    		contentvalues.put(key, new Float(value));
		    	
		    	if (type.toUpperCase().equals("LONG"))
		    		contentvalues.put(key, new Long(value));
		    	
		    	if (type.toUpperCase().equals("SHORT"))
		    		contentvalues.put(key, new Short(value));
	    	}
	    	catch (Exception e) 
	    	{
	    		Log.e("mercury", "Error with argument " + current);
	    	}
	    	
	    }
	    
	    return contentvalues;
	}
	
	//Get the columns of a content provider
	public static ArrayList<String> getColumns (ContentResolver resolver, String uri, String[] projectionArray)
	{
		//String returnValue = "";
		ArrayList<String> columns = new ArrayList<String>();
		
		try
		{				
	        //Issue query
	        Cursor c = resolver.query(Uri.parse(uri), projectionArray, null, null, null);
	                    		        	
	        //Get all column names and display
	        if (c != null)
	        {
	        	String [] colNames = c.getColumnNames();
	        	
	        	//Close the cursor
	        	c.close();
	        	
	        	//String columnNamesOutput = "";
	        	for (int k = 0; k < colNames.length; k++)
	        		columns.add(colNames[k]);
	        }
		}
		catch (Throwable t) {}
		
		return columns;
		

	}
	
	static {
		System.loadLibrary("mstring");
	}
	
	private static native String native_strings(String path);
	
	public static ArrayList<String> strings(String path) {
		ArrayList<String> lines = new ArrayList<String>();
		
		String nativeList = native_strings(path);
		
		if (nativeList != null) {		
			String[] stringList = nativeList.split("\n");
				
			if (stringList != null) {		
				for (String uri : stringList) {
					lines.add(uri);
				}
			}
		}
		
		return lines;
	}
			
	//Parse a generic intent and add to given intent
	public static Intent parseIntentGeneric(List<ArgumentWrapper> argsArray, Intent intent)
	{		
		Intent localIntent = intent;
		Iterator<ArgumentWrapper> it = argsArray.iterator();
		
		//Iterate through arguments
		while (it.hasNext())
		{
			ArgumentWrapper arg = it.next();
			
			String key = "";
			String value = "";
			
			try
			{
			
				//Try split value into key:value pair
				try
				{
					String[] split = new String(arg.value).split("=");
					key = split[0];
					value = split[1];
				}
				catch (Exception e) {}
				
				//Parse arguments into Intent
				if (arg.type.toUpperCase().equals("ACTION"))
					localIntent.setAction(new String(arg.value));
				
				if (arg.type.toUpperCase().equals("DATA"))
					localIntent.setData(Uri.parse(new String(arg.value)));
					
				if (arg.type.toUpperCase().equals("MIMETYPE"))
					localIntent.setType(new String(arg.value));

				if (arg.type.toUpperCase().equals("CATEGORY"))
					localIntent.addCategory(new String(arg.value));
					
				if (arg.type.toUpperCase().equals("COMPONENT"))
					localIntent.setComponent(new ComponentName(key, value));
					
				if (arg.type.toUpperCase().equals("FLAGS"))
					localIntent.setFlags(Integer.parseInt(new String(arg.value)));
					
				if (arg.type.toUpperCase().equals("EXTRABOOLEAN"))
					localIntent.putExtra(key, Boolean.parseBoolean(value));
					
				if (arg.type.toUpperCase().equals("EXTRABYTE"))
					localIntent.putExtra(key, Byte.parseByte(value));
					
				if (arg.type.toUpperCase().equals("EXTRADOUBLE"))
					localIntent.putExtra(key, Double.parseDouble(value));
					
				if (arg.type.toUpperCase().equals("EXTRAFLOAT"))
					localIntent.putExtra(key, Float.parseFloat(value));
					
				if (arg.type.toUpperCase().equals("EXTRAINTEGER"))
					localIntent.putExtra(key, Integer.parseInt(value));
					
				if (arg.type.toUpperCase().equals("EXTRALONG"))
					localIntent.putExtra(key, Long.parseLong(value));
					
				if (arg.type.toUpperCase().equals("EXTRASERIALIZABLE"))
					localIntent.putExtra(key, Serializable.class.cast(value));
					
				if (arg.type.toUpperCase().equals("EXTRASHORT"))
					localIntent.putExtra(key, Short.parseShort(value));
					
				if (arg.type.toUpperCase().equals("EXTRASTRING"))
					localIntent.putExtra(key, value);
					
			}
			catch (Exception e)
			{
				Log.e("mercury", "Error with argument " + arg.type + "--" + new String(arg.value));
			}
			
			
		}
		
		return localIntent;
	}
	
	//Parse a generic intent and add to given intent
	public static Intent parseIntentGeneric2(List<KVPair> argsArray, Intent intent)
	{		
		Intent localIntent = intent;
		
		//Iterate through arguments
		for (KVPair pair : argsArray)
		{
			
			String value = "";
			String valueArg = "";
			
			try
			{
				String key = pair.getKey();
				for (ByteString valueBytes : pair.getValueList()) {
					
					//Try split value into key=value pair
					String[] split = new String(valueBytes.toByteArray()).split("=");
					value = split[0];
					if (split.length > 1)
						valueArg = split[1];
					
					//Parse arguments into Intent
					if (key.equalsIgnoreCase("ACTION"))
						localIntent.setAction(value);
					
					else if (key.equalsIgnoreCase("DATA"))
						localIntent.setData(Uri.parse(value));
						
					else if (key.equalsIgnoreCase("MIMETYPE"))
						localIntent.setType(value);
	
					else if (key.equalsIgnoreCase("CATEGORY"))
						localIntent.addCategory(value);
						
					else if (key.equalsIgnoreCase("COMPONENT"))
						localIntent.setComponent(new ComponentName(value, valueArg));
						
					else if (key.equalsIgnoreCase("FLAGS"))
						localIntent.setFlags(Integer.parseInt(new String(value)));
						
					else if (key.equalsIgnoreCase("EXTRABOOLEAN"))
						localIntent.putExtra(value, Boolean.parseBoolean(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRABYTE"))
						localIntent.putExtra(value, Byte.parseByte(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRADOUBLE"))
						localIntent.putExtra(value, Double.parseDouble(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRAFLOAT"))
						localIntent.putExtra(value, Float.parseFloat(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRAINTEGER"))
						localIntent.putExtra(value, Integer.parseInt(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRALONG"))
						localIntent.putExtra(value, Long.parseLong(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRASERIALIZABLE"))
						localIntent.putExtra(value, Serializable.class.cast(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRASHORT"))
						localIntent.putExtra(value, Short.parseShort(valueArg));
						
					else if (key.equalsIgnoreCase("EXTRASTRING"))
						localIntent.putExtra(value, valueArg);
						
				}
			}
			catch (Exception e)
			{
				Log.e("mercury", "Error with argument " + pair.getKey());
			}
			
		}
		
		return localIntent;
	}

	//Extract the src file to dest - return success
	public static boolean unzipFile(String filename, String src, String dest)
	{
		final int BUFFER_SIZE = 4096;
		boolean success = false;
		String fname = filename.toUpperCase();
		  
		BufferedOutputStream bufferedOutputStream = null;
		FileInputStream fileInputStream;
		try
		{
			fileInputStream = new FileInputStream(src);
			ZipInputStream zipInputStream = new ZipInputStream(new BufferedInputStream(fileInputStream));
			ZipEntry zipEntry;
		      
			while ((zipEntry = zipInputStream.getNextEntry()) != null)
			{
				String zipEntryName = zipEntry.getName();
				if (zipEntryName.toUpperCase().equals(fname))
				{
					File file = new File(dest + zipEntryName);
					byte buffer[] = new byte[BUFFER_SIZE];
					FileOutputStream fileOutputStream = new FileOutputStream(file);
					bufferedOutputStream = new BufferedOutputStream(fileOutputStream, BUFFER_SIZE);
					int count;

					while ((count = zipInputStream.read(buffer, 0, BUFFER_SIZE)) != -1)
					{
						bufferedOutputStream.write(buffer, 0, count);
					}

					bufferedOutputStream.flush();
					bufferedOutputStream.close();
					
					success = true;
				}

			}
			zipInputStream.close();
		}
		catch (Exception e)
		{
			Log.e("mercury", e.getMessage());
		}

			   
		return success;

	}
	
	public static KVPair createKVPair(String key, String value) {
		return createKVPair(key, ByteString.copyFrom(value.getBytes()));
	}
	
	public static KVPair createKVPair(String key, List<String> values) {
		KVPair.Builder pairBuilder = KVPair.newBuilder();
		pairBuilder.setKey(key);
		for (String value : values)
			pairBuilder.addValue(ByteString.copyFrom(value.getBytes()));
		return pairBuilder.build();
	}
	
	public static KVPair createKVPair(String key, ByteString value) {
		KVPair.Builder pairBuilder = KVPair.newBuilder();
		pairBuilder.setKey(key);
		pairBuilder.addValue(value);
		return pairBuilder.build();
	}

}
