// License: Refer to the README in the root directory

package com.mwr.mercury.commands;

import com.google.protobuf.ByteString;
import com.mwr.mercury.ArgumentWrapper;
import com.mwr.mercury.Common;
import com.mwr.mercury.Message.KVPair;
import com.mwr.mercury.Message.Request;
import com.mwr.mercury.Message.Response;
import com.mwr.mercury.Session;

import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.pm.PackageManager;
import android.content.pm.PathPermission;
import android.content.pm.ProviderInfo;
import android.database.Cursor;
import android.net.Uri;
import android.os.PatternMatcher;
import android.util.Base64;
import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class Provider
{
	/*
	public static void info(List<KVPair> argsArray, Session currentSession)
	{
		String filter = Common.getParamString2(argsArray, "filter");
		String permissions = Common.getParamString2(argsArray, "permissions");
		
		// Get all providers and iterate through them
		List<ProviderInfo> providers = currentSession.applicationContext
				.getPackageManager().queryContentProviders(null,
						PackageManager.GET_URI_PERMISSION_PATTERNS,
						PackageManager.GET_URI_PERMISSION_PATTERNS);

		Request.Builder reqBuilder = Request.newBuilder();
		// Iterate through content providers
		for (int i = 0; i < providers.size(); i++)
		{
			// Get all relevant info from content provider
			String providerAuthority = providers.get(i).authority;
			String providerPackage = providers.get(i).packageName;
			String providerReadPermission = providers.get(i).readPermission;
			PatternMatcher[] uriPermissionPatterns = providers.get(i).uriPermissionPatterns;
			String providerWritePermission = providers.get(i).writePermission;
			PathPermission[] providerPathPermissions = providers.get(i).pathPermissions;
			boolean providerMultiprocess = providers.get(i).multiprocess;
			boolean grantUriPermissions = providers.get(i).grantUriPermissions;

			boolean relevantFilter = false;
			boolean relevantPermissions = false;
			boolean noFilters = false;
			boolean bothFiltersRelevant = false;

			// Check if a filter was used
			if (filter.length() > 0)
				relevantFilter = providerAuthority.toUpperCase().contains(
						filter.toUpperCase())
						|| providerPackage.toUpperCase().contains(
								filter.toUpperCase());

			// Check if a permission filter was used
			try
			{
				if (permissions.length() > 0)
				{
					if (permissions.toUpperCase().equals("NULL"))
						relevantPermissions = (providerReadPermission == null)
								|| (providerWritePermission == null);
					else
						relevantPermissions = providerReadPermission.toUpperCase()
								.contains(permissions.toUpperCase())
								|| providerWritePermission.toUpperCase()
										.contains(permissions.toUpperCase());
				}
			}
			catch (Throwable t)
			{
			}

			// Check if no parameters were given
			if (filter.length() == 0 && permissions.length() == 0)
				noFilters = true;

			boolean bothFiltersPresent = false;
			if ((filter != "") && (permissions != ""))
				bothFiltersPresent = true;

			if (bothFiltersPresent && relevantFilter && relevantPermissions)
				bothFiltersRelevant = true;

			// Apply filter and only look @ exported providers
			if (((bothFiltersPresent && bothFiltersRelevant)
					|| (!bothFiltersPresent && (relevantFilter || relevantPermissions)) || (!bothFiltersPresent && noFilters))
					&& providers.get(i).exported)
			{
				
				// URI Permission Patterns
				if (uriPermissionPatterns != null)
					for (int j = 0; j < uriPermissionPatterns.length; j++)
					{
						String path = uriPermissionPatterns[j].getPath();
						ByteString bsPath = ByteString.copyFrom(path.getBytes());
						if (path != null) {
							reqBuilder.addArgs(KVPair.newBuilder()
											.setKey("uriPermissionPattern")
											.setValue(bsPath));
						}
					}
				
				// Path permissions
				if (providerPathPermissions != null) 
					for (int j = 0; j < providerPathPermissions.length; j++)
					{
						if (providerPathPermissions[j].getReadPermission() != null)
						{
							String value = providerPathPermissions[j].getPath() + "-" + 
										   providerPathPermissions[j].getReadPermission();
							ByteString bsValue = ByteString.copyFrom(value.getBytes());
							reqBuilder.addArgs(KVPair.newBuilder()
									.setKey("pathReadPermission")
									.setValue(bsValue));
						}

						if (providerPathPermissions[j].getWritePermission() != null)
						{
							String value = providerPathPermissions[j].getPath() + "-" + 
							   			   providerPathPermissions[j].getWritePermission();
							ByteString bsValue = ByteString.copyFrom(value.getBytes());
							reqBuilder.addArgs(KVPair.newBuilder()
									.setKey("pathWritePermission")
									.setValue(bsValue));
						}
					}
				
				if (providerReadPermission != null) 
				{
					ByteString bsValue = ByteString.copyFrom(providerReadPermission.getBytes());
					reqBuilder.addArgs(KVPair.newBuilder()
							.setKey("readPermission")
							.setValue(bsValue));
				}
				if (providerWritePermission != null)
				{
					ByteString bsValue = ByteString.copyFrom(providerWritePermission.getBytes());
					reqBuilder.addArgs(KVPair.newBuilder()
							.setKey("writePermission")
							.setValue(bsValue));
				}
				reqBuilder.addArgs(KVPair.newBuilder()
						.setKey("grantUriPermission")
						.setValue(ByteString.copyFrom(new Boolean(grantUriPermissions).toString().getBytes())));
				reqBuilder.addArgs(KVPair.newBuilder()
						.setKey("multiprocess")
						.setValue(ByteString.copyFrom(new Boolean(providerMultiprocess).toString().getBytes())));
				reqBuilder.setMultiprocess(new Boolean(grantUriPermissions).toString().getBytes());
				reqBuilder.build().toByteString();
				provBuilder.addInfo(infoBuilder.build());			
			}
		}
		
		Response resp = Response.newBuilder().setProviderResponse(provBuilder.build()).build();
		currentSession.send(Base64.encodeToString(resp.toByteArray(), Base64.DEFAULT), false);
		
	}
*/
	public static void columns(List<KVPair> argsArray,
			Session currentSession)
	{
		// Get list of columns
		ArrayList<String> columns = Common.getColumns(
				currentSession.applicationContext.getContentResolver(),
				Common.getParamString2(argsArray, "uri"), null);

		Response.Builder respBuilder = Response.newBuilder();

		if (columns.size() == 0)
		{
			ByteString bs = ByteString.copyFrom("Invalid content URI specified".getBytes());
			respBuilder.setError(bs);
		}
		else
		{
			KVPair.Builder pairBuilder = KVPair.newBuilder();
			// Iterate through columns
			for (int i = 0; i < columns.size(); i++)
			{
				pairBuilder.addValue(ByteString.copyFrom(columns.get(i).getBytes()));
			}
			respBuilder.setError(ByteString.copyFrom("Success".getBytes()));
		}
		
		Response resp = respBuilder.build();
		currentSession.send(Base64.encodeToString(resp.toByteArray(), Base64.DEFAULT), false);
	}

	public static void query(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		currentSession.startTransmission();
		currentSession.startResponse();
		currentSession.startData();

		try
		{
			// Get content provider and cursor
			ContentResolver r = currentSession.applicationContext
					.getContentResolver();

			// Get all the parameters
			List<String> projection = Common.getParamStringList(argsArray,
					"projection");
			String selection = Common.getParamString(argsArray, "selection");
			List<String> selectionArgs = Common.getParamStringList(argsArray,
					"selectionArgs");
			String sortOrder = Common.getParamString(argsArray, "sortOrder");
			String showColumns = Common
					.getParamString(argsArray, "showColumns");

			// Put projection in an array
			String[] projectionArray = null;
			if (projection.size() > 0)
			{
				projectionArray = new String[projection.size()];
				Iterator<String> it = projection.iterator();

				int i = 0;

				while (it.hasNext())
				{
					projectionArray[i] = it.next();
					i++;
				}
			}

			// Put selectionArgs in an array
			String[] selectionArgsArray = null;
			if (selectionArgs.size() > 0)
			{
				selectionArgsArray = new String[selectionArgs.size()];
				Iterator<String> it = selectionArgs.iterator();

				int i = 0;

				while (it.hasNext())
				{
					selectionArgsArray[i] = it.next();
					i++;
				}
			}

			// Issue query
			Cursor c = r.query(Uri.parse(new String(Common.getParam(argsArray,
					"Uri"))), projectionArray,
					(selection.length() > 0) ? selection : null,
					selectionArgsArray, (sortOrder.length() > 0) ? sortOrder
							: null);

			// Check if query failed
			if (c != null)
			{
				// Display the columns
				if (showColumns.length() == 0
						|| showColumns.toUpperCase().contains("TRUE"))
				{
					ArrayList<String> cols = Common.getColumns(r,
							Common.getParamString(argsArray, "Uri"),
							projectionArray);
					Iterator<String> it = cols.iterator();
					String columns = "";

					while (it.hasNext())
						columns += it.next() + " | ";

					currentSession.send(
							columns.substring(0, columns.length() - 3), true);
					currentSession.send("\n.....\n\n", true);
				}

				// Get all rows of data
				for (c.moveToFirst(); !c.isAfterLast(); c.moveToNext())
				{
					int numOfColumns = c.getColumnCount();
					String data = "";

					// Iterate through columns
					for (int l = 0; l < numOfColumns; l++)
					{

						// Get string - if there is an error try retrieve as a
						// blob
						try
						{
							data += c.getString(l);
						}
						catch (Exception e)
						{
							// Base64 encode blobs and prepend with (blob)
							data += "(blob) "
									+ Base64.encodeToString(c.getBlob(l),
											Base64.DEFAULT);
						}

						// Check if a column separator should be added or not
						if (l != (numOfColumns - 1))
							data += " | ";
					}

					currentSession.send(data + "\n\n", true);
				}

				currentSession.endData();
				currentSession.noError();
			}
			else
			{
				currentSession.endData();
				currentSession.error("Query failed");
			}

		}
		catch (Throwable t)
		{
			currentSession.endData();
			currentSession.error(t.getMessage());
		}

		currentSession.endResponse();
		currentSession.endTransmission();
	}

	public static void read(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		// Start transmission
		currentSession.startTransmission();
		currentSession.startResponse();
		currentSession.startData();

		try
		{
			Uri uri = Uri.parse(Common.getParamString(argsArray, "Uri"));
			ContentResolver r = currentSession.applicationContext
					.getContentResolver();
			InputStream is = r.openInputStream(uri);
			ByteArrayOutputStream baos = new ByteArrayOutputStream();
			int len = -1;
			do
			{
				byte[] buf = new byte[1024];
				len = is.read(buf);
				if (len > 0)
					baos.write(buf, 0, len);

			}
			while (len != -1);

			byte[] buf = baos.toByteArray();
			String b64 = Base64.encodeToString(buf, 0);

			// Send response
			currentSession.send(b64, false);
			currentSession.endData();
			currentSession.noError();
		}
		catch (Throwable t)
		{
			currentSession.endData();
			currentSession.error(t.getMessage());
		}
		finally
		{
			currentSession.endResponse();
			currentSession.endTransmission();
		}
	}

	public static void insert(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		try
		{
			ContentValues contentvalues = new ContentValues();

			// Place values into contentvalue structure
			List<String> strings = Common.getParamStringList(argsArray,
					"string");
			if (strings != null)
				contentvalues.putAll(Common.listToContentValues(strings,
						"string"));

			List<String> booleans = Common.getParamStringList(argsArray,
					"boolean");
			if (booleans != null)
				contentvalues.putAll(Common.listToContentValues(booleans,
						"boolean"));

			List<String> integers = Common.getParamStringList(argsArray,
					"integer");
			if (integers != null)
				contentvalues.putAll(Common.listToContentValues(integers,
						"integer"));

			List<String> doubles = Common.getParamStringList(argsArray,
					"double");
			if (doubles != null)
				contentvalues.putAll(Common.listToContentValues(doubles,
						"double"));

			List<String> floats = Common.getParamStringList(argsArray, "float");
			if (floats != null)
				contentvalues.putAll(Common
						.listToContentValues(floats, "float"));

			List<String> longs = Common.getParamStringList(argsArray, "long");
			if (longs != null)
				contentvalues.putAll(Common.listToContentValues(longs, "long"));

			List<String> shorts = Common.getParamStringList(argsArray, "short");
			if (shorts != null)
				contentvalues.putAll(Common
						.listToContentValues(shorts, "short"));

			// Get content resolver
			ContentResolver r = currentSession.applicationContext
					.getContentResolver();

			// Issue insert command
			Uri c = r.insert(
					Uri.parse(new String(Common.getParam(argsArray, "Uri"))),
					contentvalues);

			currentSession.sendFullTransmission(c.toString(), "");

		}
		catch (Throwable t)
		{
			currentSession.sendFullTransmission("", t.getMessage());
		}
	}

	public static void update(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		try
		{
			ContentValues contentvalues = new ContentValues();

			// Place values into contentvalue structure
			List<String> strings = Common.getParamStringList(argsArray,
					"string");
			if (strings != null)
				contentvalues.putAll(Common.listToContentValues(strings,
						"string"));

			List<String> booleans = Common.getParamStringList(argsArray,
					"boolean");
			if (booleans != null)
				contentvalues.putAll(Common.listToContentValues(booleans,
						"boolean"));

			List<String> integers = Common.getParamStringList(argsArray,
					"integer");
			if (integers != null)
				contentvalues.putAll(Common.listToContentValues(integers,
						"integer"));

			List<String> doubles = Common.getParamStringList(argsArray,
					"double");
			if (doubles != null)
				contentvalues.putAll(Common.listToContentValues(doubles,
						"double"));

			List<String> floats = Common.getParamStringList(argsArray, "float");
			if (floats != null)
				contentvalues.putAll(Common
						.listToContentValues(floats, "float"));

			List<String> longs = Common.getParamStringList(argsArray, "long");
			if (longs != null)
				contentvalues.putAll(Common.listToContentValues(longs, "long"));

			List<String> shorts = Common.getParamStringList(argsArray, "short");
			if (shorts != null)
				contentvalues.putAll(Common
						.listToContentValues(shorts, "short"));

			List<String> selectionArgs = Common.getParamStringList(argsArray,
					"selectionArgs");
			String where = Common.getParamString(argsArray, "where");

			// Put selectionArgs in an array
			String[] selectionArgsArray = null;
			if (selectionArgs.size() > 0)
			{
				selectionArgsArray = new String[selectionArgs.size()];
				Iterator<String> it = selectionArgs.iterator();

				int i = 0;

				while (it.hasNext())
				{
					selectionArgsArray[i] = it.next();
					i++;
				}
			}

			// Get content resolver
			ContentResolver r = currentSession.applicationContext
					.getContentResolver();

			// Issue update command
			Integer c = r.update(
					Uri.parse(Common.getParamString(argsArray, "Uri")),
					contentvalues, (where.length() > 0) ? where : null,
					selectionArgsArray);

			// Send response
			currentSession.sendFullTransmission(c.toString()
					+ " rows have been updated.", "");

		}
		catch (Throwable t)
		{
			currentSession.sendFullTransmission("", t.getMessage());
		}
	}

	public static void delete(List<ArgumentWrapper> argsArray,
			Session currentSession)
	{
		try
		{

			List<String> selectionArgs = Common.getParamStringList(argsArray,
					"selectionArgs");
			String where = Common.getParamString(argsArray, "where");

			// Put selectionArgs in an array
			String[] selectionArgsArray = null;
			if (selectionArgs.size() > 0)
			{
				selectionArgsArray = new String[selectionArgs.size()];
				Iterator<String> it = selectionArgs.iterator();

				int i = 0;

				while (it.hasNext())
				{
					selectionArgsArray[i] = it.next();
					i++;
				}
			}

			// Get content resolver
			ContentResolver r = currentSession.applicationContext
					.getContentResolver();

			// Issue delete command
			int rowsDeleted = r.delete(
					Uri.parse(Common.getParamString(argsArray, "Uri")),
					(where.length() > 0) ? where : null, selectionArgsArray);

			// Send response
			currentSession.sendFullTransmission(Integer.toString(rowsDeleted)
					+ " rows have been deleted", "");

		}
		catch (Throwable t)
		{
			currentSession.sendFullTransmission("", t.getMessage());
		}

		currentSession.endTransmission();
	}

public static void finduri(List<ArgumentWrapper> argsArray, Session currentSession)
{
	//Get path from arguments
	String path = Common.getParamString(argsArray, "path");
	
	ArrayList<String> lines = Common.strings(path);
	Iterator<String> it = lines.iterator();
	
	currentSession.startTransmission();
	currentSession.startResponse();
	currentSession.startData();
	
	while (it.hasNext())
	{
		String next = it.next();
		
		if (next.toUpperCase().contains("CONTENT://") && !next.toUpperCase().equals("CONTENT://"))
			currentSession.send(next + "\n", true); //Send content uri with newline
	}
	
	currentSession.endData();
	currentSession.noError();
	currentSession.endResponse();
	currentSession.endTransmission();
}

}