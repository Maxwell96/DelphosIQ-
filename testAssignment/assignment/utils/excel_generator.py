def generate_workbook(workbook_name, sheet_data, sheet_data_headers, chart_data, chart_data_headers):
    import xlsxwriter

    # Creating workbook
    workbook = xlsxwriter.Workbook(workbook_name)

    # Creating worksheets
    data_sheet = workbook.add_worksheet("Data sheet")

    title_format = workbook.add_format()
    title_format.set_bold()
    title_format.set_font_size(12)
    title_format.set_align('center')

    entries_format = workbook.add_format()
    entries_format.set_align('center')

    # Adding headers
    for i, header in enumerate(sheet_data_headers):
        data_sheet.write(0, i, str(header).upper(), title_format)

    # Adding entries
    for j, row_data in enumerate(sheet_data):
        for i, entry in enumerate(row_data):
            data_sheet.write(i + 1, j, entry, entries_format)

    data_sheet.autofit()



    # CREATING CHART.
    """(Wanted to extract the chart creation to a different function. Meaning I will have to access an already 
     existing workbook but xlsxwriter cannot be used to edit an existing Excel file). Unless I use Openpyxl which 
     was not stated as part of the tools to use."""
    # Creating chart sheet
    chart_sheet = workbook.add_worksheet('Chartsheet')

    # Creating dummy sheet for the charts
    dummy_sheet = workbook.add_worksheet("Dummysheet")
    col = 0
    for i, queryset in enumerate(chart_data):  # For every queryset in the chart_data
        headers = chart_data_headers[i]  # Find the corresponding header list from the chart_data_headers
        for j, entry in enumerate(queryset):  # For every entry in the queryset
            dummy_sheet.write(j, col, entry[headers[0]])
            dummy_sheet.write(j, col+1, entry[headers[1]])
        col += 2

    # Creating a chat object
    chart = workbook.add_chart({"type": "column"})

    # Creating dynamic data to be used for the chart series as defined names
    chart_x_label = f'=IF(Chartsheet!$A$1="By Year",\
                Dummysheet!$B$1:$B${len(chart_data[0]) + 1},\
                IF(Chartsheet!$A$1="By Country",\
                Dummysheet!$D$1:$D${len(chart_data[1]) + 1},\
                Dummysheet!$F$1:$F${len(chart_data[2]) + 1}\
            )\
        )'

    chart_y_label = f'=IF(Chartsheet!$A$1="By Year",\
                Dummysheet!$A$1:$A${len(chart_data[0]) + 1},\
                IF(Chartsheet!$A$1="By Country",\
                Dummysheet!$C$1:$C${len(chart_data[1]) + 1},\
                Dummysheet!$E$1:$E${len(chart_data[2]) + 1}\
            )\
        )'

    # Creating named ranges for the data in each sheet
    workbook.define_name("chart_series", chart_y_label)
    workbook.define_name("chart_labels", chart_x_label)

    # Adding a drop-down list for selecting the data to display
    chart_sheet.data_validation("A1", {"validate": "list",
                                       "source": ["By Year", "By Country", "By Sector"],
                                       "input_title": "Select Data",
                                       "input_message": "Select data to display in chart"})

    # Adding dropdown format
    dropdown_format = workbook.add_format(
        {"bg_color": "black", "bold": True, "align": "center", "font_color": "white"}
    )

    # Setting default value to the cell
    chart_sheet.write("A1", "By Year", dropdown_format)

    # Configuring the data series for the chart
    chart.add_series({
        'values': '=Dummysheet!chart_labels',
        'categories': '=Dummysheet!chart_series',
        'name': 'Selected Data',
    })

    # Formatting chart
    chart.set_size({"width": 720, "height": 350})
    chart.set_style(8)
    chart.set_legend({"none": True})

    # Inserting the charts into the chart sheet
    chart_sheet.insert_chart("E3", chart)

    # Hiding dummy sheet
    dummy_sheet.hide()

    workbook.close()
