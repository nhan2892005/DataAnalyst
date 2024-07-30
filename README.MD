# VBA Module Process Data in Excel

<details>
<summary><code>Sub CopyUniqueValuesBetweenColumns()</code></summary>

```
Sub CopyUniqueValuesBetweenColumns()
    Dim ws As Worksheet
    Dim sourceCol As String
    Dim destCol As String
    Dim sourceRange As Range
    Dim destRange As Range
    Dim cell As Range
    Dim uniqueValues As Collection
    Dim item As Variant
    Dim destRow As Long
    Dim lastRowSource As Long
    Dim lastRowDest As Long
    
    ' Set ws to the currently active sheet
    Set ws = ActiveSheet

    ' Input source and destination column names from the user
    sourceCol = InputBox("Enter the source column (e.g., E):", "Input Source Column")
    destCol = InputBox("Enter the destination column (e.g., P):", "Input Destination Column")

    ' Check user input
    If sourceCol = "" Or destCol = "" Then
        MsgBox "You must enter both the source and destination columns.", vbExclamation
        Exit Sub
    End If

    ' Determine the last row in the source and destination columns
    lastRowSource = ws.Cells(ws.Rows.Count, sourceCol).End(xlUp).Row
    lastRowDest = ws.Cells(ws.Rows.Count, destCol).End(xlUp).Row

    ' Define the source and destination ranges
    Set sourceRange = ws.Range(sourceCol & "1:" & sourceCol & lastRowSource)
    Set destRange = ws.Range(destCol & "1")

    ' Initialize the Collection to store unique values
    Set uniqueValues = New Collection

    On Error Resume Next ' Ignore errors if the value already exists in the Collection

    ' Loop through each cell in the source range
    For Each cell In sourceRange
        ' Add value to Collection if it does not already exist
        uniqueValues.Add cell.Value, CStr(cell.Value)
    Next cell

    On Error GoTo 0 ' Stop ignoring errors

    ' Clear existing data in the destination column
    ws.Range(destCol & "1:" & destCol & lastRowDest).Clear

    ' Copy unique values to the destination column
    destRow = 1 ' Start at row 1 in the destination column
    For Each item In uniqueValues
        ws.Cells(destRow, destCol).Value = item
        destRow = destRow + 1
    Next item
End Sub
```

</details>

<details>
<summary><code>Sub CopyAndDistributeMergedCellsToAnotherSheet()</code></summary>

```
Sub CopyAndDistributeMergedCellsToAnotherSheet()
    Dim sourceSheet As String
    Dim destSheet As String
    Dim wsSource As Worksheet
    Dim wsDest As Worksheet
    Dim cell As Range
    Dim mergeArea As Range
    Dim r As Long, c As Long
    Dim lastRowSource As Long
    Dim lastColSource As Long
    Dim processedAreas As Collection
    Dim key As String
    
    ' Input source and destination column names from the user
    sourceSheet = InputBox("Enter the source sheet :", "Input Source Sheet")
    destSheet = InputBox("Enter the destination sheet :", "Input Destination Sheet")

    ' Check user input
    If sourceSheet = "" Or destSheet = "" Then
        MsgBox "You must enter both the source and destination columns.", vbExclamation
        Exit Sub
    End If
    
    Set wsSource = ThisWorkbook.Sheets(sourceSheet) ' Change source sheet name if needed
    Set wsDest = ThisWorkbook.Sheets(destSheet) ' Change destination sheet name if needed
    
    wsDest.Cells.Clear

    ' Determine the last row and column with data in the source sheet
    lastRowSource = wsSource.Cells(wsSource.Rows.Count, 1).End(xlUp).Row
    lastColSource = wsSource.Cells(1, wsSource.Columns.Count).End(xlToLeft).Column
    
    ' Hardcoded last row and column
    lastRowSource = 351
    lastColSource = 14
    
    ' Initialize the collection to keep track of processed merged areas
    Set processedAreas = New Collection

    For r = 1 To lastRowSource
        For c = 1 To lastColSource
            Set cell = wsSource.Cells(r, c)
            
            If cell.MergeCells Then
                Set mergeArea = cell.mergeArea
                key = CStr(mergeArea.Address) ' Create a unique key for the merged area
                
                On Error Resume Next
                processedAreas.Add key, key
                If Err.Number = 0 Then
                    ' Copy merged cell value to the destination sheet
                    wsDest.Range(wsDest.Cells(mergeArea.Row, mergeArea.Column), _
                                 wsDest.Cells(mergeArea.Row + mergeArea.Rows.Count - 1, _
                                              mergeArea.Column + mergeArea.Columns.Count - 1)).Value = cell.Value
                End If
                On Error GoTo 0
            Else
                ' Copy non-merged cell value to the destination sheet
                wsDest.Cells(r, c).Value = cell.Value
            End If
        Next c
    Next r
End Sub
```
</details>

<details>
<summary><code>Sub TransferToNewSheet()</code></summary>

```
Sub TransferToNewSheet()
    Dim wsSource As Worksheet
    Dim wsDest As Worksheet
    Dim lastRow As Long
    Dim i As Long
    Dim j As Long
    Dim c As Range
    Dim pValues As Collection
    Dim qValues As Collection
    Dim p As Variant
    Dim q As Variant
    Dim destRow As Long
    Dim destCol As Long
    Dim userInputSheet As String
    Dim wsSourceStr As String
    
    ' Prompt for the destination sheet name
    wsSourceStr = InputBox("Enter the name of the source sheet:", "Enter Destination Sheet Name")
    userInputSheet = InputBox("Enter the name of the destination sheet:", "Enter Destination Sheet Name")
    
    ' Check for user input
    If userInputSheet = "" Or wsSourceStr = "" Then
        MsgBox "You must enter the name of the source or destination sheet.", vbExclamation
        Exit Sub
    End If
    
    ' Set source and destination worksheets
    Set wsSource = ThisWorkbook.Sheets(wsSourceStr)
    On Error Resume Next
    Set wsDest = ThisWorkbook.Sheets(userInputSheet)
    On Error GoTo 0
    
    If wsDest Is Nothing Then
        ' Create the destination sheet if it does not exist
        Set wsDest = ThisWorkbook.Sheets.Add(After:=ThisWorkbook.Sheets(ThisWorkbook.Sheets.Count))
        wsDest.Name = userInputSheet
    Else
        ' Clear existing data if the destination sheet already exists
        wsDest.Cells.Clear
    End If
    
    ' Determine the last row in columns P and Q
    lastRow = wsSource.Cells(wsSource.Rows.Count, "P").End(xlUp).Row
    
    ' Create collections to store unique values
    Set pValues = New Collection
    Set qValues = New Collection
    
    ' Retrieve unique values from columns P and Q
    On Error Resume Next
    For i = 1 To lastRow
        pValues.Add wsSource.Cells(i, "P").Value, CStr(wsSource.Cells(i, "P").Value)
        qValues.Add wsSource.Cells(i, "Q").Value, CStr(wsSource.Cells(i, "Q").Value)
    Next i
    On Error GoTo 0
    
    ' Set column headers
    destRow = 1
    destCol = 2 ' Start from column B (column 2) to leave one column for the row labels
    For Each q In qValues
        wsDest.Cells(destRow, destCol).Value = q
        destCol = destCol + 1
    Next q
    
    ' Set row labels
    destRow = 2 ' Start from row 2
    destCol = 1
    For Each p In pValues
        wsDest.Cells(destRow, destCol).Value = p
        destRow = destRow + 1
    Next p
    
    ' Fill data into the matrix
    For i = 1 To lastRow
        For j = 1 To pValues.Count
            If wsSource.Cells(i, "P").Value = pValues(j) Then
                wsDest.Cells(Application.Match(wsSource.Cells(i, "Q").Value, wsDest.Rows(1), 0), _
                             Application.Match(wsSource.Cells(i, "P").Value, wsDest.Columns(1), 0)).Value = wsSource.Cells(i, "Q").Value
            End If
        Next j
    Next i
    
    MsgBox "Data has been successfully transferred.", vbInformation
End Sub
```
</details>

<details>
<summary><code>Sub CopyUniqueValuesBetweenColumns()</code></summary>

```
Sub CalculateTotalBasedOnConditions()
    Dim wsModel As Worksheet
    Dim wsDest As Worksheet
    Dim lastRowModel As Long
    Dim lastRowDest As Long
    Dim lastColModel As Long
    Dim modelColHeader As Range
    Dim modelRowHeader As Range
    Dim destRange As Range
    Dim cell As Range
    Dim rowCell As Range
    Dim destRow As Long
    Dim destCol As Long
    Dim i As Long
    Dim total As Double
    Dim destItemCol As Long
    Dim destAmountCol As Long
    
    ' Set worksheets
    Set wsModel = ThisWorkbook.Sheets("Model")
    Set wsDest = ThisWorkbook.Sheets("Dest")
    
    ' Determine last rows in "Model" and "Dest"
    lastRowModel = wsModel.Cells(wsModel.Rows.Count, 1).End(xlUp).Row
    lastRowDest = wsDest.Cells(wsDest.Rows.Count, 1).End(xlUp).Row
    
    ' Find the last column with data in the first row of "Model"
    lastColModel = wsModel.Cells(1, wsModel.Columns.Count).End(xlToLeft).Column
    
    ' Define header ranges in "Model"
    Set modelColHeader = wsModel.Range(wsModel.Cells(1, 2), wsModel.Cells(1, lastColModel)) ' Column headers
    Set modelRowHeader = wsModel.Range("A2:A" & lastRowModel) ' Row headers
    
    ' Define data range and columns in "Dest"
    destItemCol = wsDest.Cells(1, wsDest.Columns.Count).End(xlToLeft).Column ' Last column with data
    destAmountCol = 12 ' Column L
    
    ' Loop through column headers in "Model"
    For Each cell In modelColHeader
        If Not IsEmpty(cell.Value) Then
            ' Determine column in "Model"
            destCol = cell.Column
            
            ' Loop through row headers in "Model"
            For Each rowCell In modelRowHeader
                If Not IsEmpty(rowCell.Value) Then
                    ' Determine row in "Model"
                    destRow = rowCell.Row
                    total = 0
                    
                    ' Calculate total for each level
                    For i = 1 To lastRowDest
                        If wsDest.Cells(i, 5).Value = wsModel.Cells(destRow, 1).Value And _
                           wsDest.Cells(i, 10).Value = wsModel.Cells(1, destCol).Value Then
                            total = total + wsDest.Cells(i, destAmountCol).Value
                        End If
                    Next i
                    
                    ' Update total in "Model"
                    wsModel.Cells(destRow, destCol).Value = total
                End If
            Next rowCell
        End If
    Next cell
    
    MsgBox "Calculation complete.", vbInformation
End Sub
```

</details>