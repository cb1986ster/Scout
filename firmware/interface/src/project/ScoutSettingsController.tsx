import React, { Component } from 'react';
import { ValidatorForm, TextValidator } from 'react-material-ui-form-validator';

import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';

import { Typography, Box } from '@material-ui/core';
import SaveIcon from '@material-ui/icons/Save';

import { ENDPOINT_ROOT } from '../api';
import { restController, RestControllerProps, RestFormLoader, RestFormProps, FormActions, FormButton, SectionContent } from '../components';

import { ScoutSettings } from './types';

export const SCOUT_SETTINGS_ENDPOINT = ENDPOINT_ROOT + "scout";


type ScoutSettingsControllerProps = RestControllerProps<ScoutSettings>;

class ScoutSettingsController extends Component<ScoutSettingsControllerProps> {

  componentDidMount() {
    this.props.loadData();
  }

  render() {
    return (
      <SectionContent title='Scout Settings' titleGutter>
        <RestFormLoader
          {...this.props}
          render={props => (
            <ScoutSettingsControllerForm {...props} />
          )}
        />
      </SectionContent>
    )
  }

}

export default restController(SCOUT_SETTINGS_ENDPOINT, ScoutSettingsController);

type ScoutSettingsControllerFormProps = RestFormProps<ScoutSettings>;

function ScoutSettingsControllerForm(props: ScoutSettingsControllerFormProps) {
  const { data, saveData, handleValueChange } = props;

  const ServoSettingsRow = (
      servo_number:string,
      min_value:keyof ScoutSettings,
      max_value:keyof ScoutSettings,
      pin_value:keyof ScoutSettings,
      data:ScoutSettings
  ) => {
      return (
          <TableRow key={pin_value}>
              <TableCell component="th" scope="row">
                  {servo_number}
              </TableCell>
               <TableCell align="right">
                  <TextValidator
                    validators={['required', 'isNumber', 'minNumber:100', 'maxNumber:1024']}
                    errorMessages={['Minimal frequency is required','Must be a number','Minimum value: 100','Maximal value: 1024']}
                    name={min_value}
                    label="Minimal frequency"
                    variant="outlined"
                    value={data[min_value]}
                    type="number"
                    onChange={handleValueChange(min_value)}
                    margin="normal"
                  />
              </TableCell>
               <TableCell align="right">
                  <TextValidator
                    validators={['required', 'isNumber', 'minNumber:100', 'maxNumber:1024']}
                    errorMessages={['Maximal frequency is required','Must be a number','Minimum value: 100','Maximal value: 1024']}
                    name={max_value}
                    label="Maximal frequency"
                    variant="outlined"
                    value={data[max_value]}
                    type="number"
                    onChange={handleValueChange(max_value)}
                    margin="normal"
                  />
              </TableCell>
               <TableCell align="right">
                  <TextValidator
                    validators={['required', 'isNumber', 'minNumber:0', 'maxNumber:15']}
                    errorMessages={['Pin number is required','Must be a number','Minimum value: 0','Maximal value: 15']}
                    name={pin_value}
                    label="Pin number"
                    variant="outlined"
                    value={data[pin_value]}
                    type="number"
                    onChange={handleValueChange(pin_value)}
                    margin="normal"
                  />
              </TableCell>
          </TableRow>
      );
  }

  return (
    <ValidatorForm onSubmit={saveData}>
      <Box bgcolor="primary.main" color="primary.contrastText" p={2} mt={2} mb={2}>
        <Typography variant="body1">
          Here you have all pinout and servo settings.
        </Typography>
      </Box>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
            <TableBody>
            {ServoSettingsRow("Front right base","min_00","max_00","pin_00",data)}
            {ServoSettingsRow("Front right arm","min_01","max_01","pin_01",data)}
            {ServoSettingsRow("Front right foot","min_02","max_02","pin_02",data)}
            {ServoSettingsRow("Front left base","min_03","max_03","pin_03",data)}
            {ServoSettingsRow("Front left arm","min_04","max_04","pin_04",data)}
            {ServoSettingsRow("Front left foot","min_05","max_05","pin_05",data)}
            {ServoSettingsRow("Back left base","min_06","max_06","pin_06",data)}
            {ServoSettingsRow("Back left arm","min_07","max_07","pin_07",data)}
            {ServoSettingsRow("Back left foot","min_08","max_08","pin_08",data)}
            {ServoSettingsRow("Back right base","min_09","max_09","pin_09",data)}
            {ServoSettingsRow("Back right arm","min_10","max_10","pin_10",data)}
            {ServoSettingsRow("Back right foot","min_11","max_11","pin_11",data)}
        </TableBody>
      </Table>
    </TableContainer>
      <FormActions>
        <FormButton startIcon={<SaveIcon />} variant="contained" color="primary" type="submit">
          Save
        </FormButton>
      </FormActions>
    </ValidatorForm>
  );
}
