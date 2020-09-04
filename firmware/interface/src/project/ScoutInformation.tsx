import React, { Component } from 'react';
import { Typography, Box} from '@material-ui/core';
import { SectionContent } from '../components';

class ScoutInformation extends Component {

  render() {
    return (
      <SectionContent title='Scout Information' titleGutter>
        <Typography variant="body1" paragraph>
          This simple project allows you to control You quadruper robot.
        </Typography>
        <Box mt={2}>
          <Typography variant="body2">
            TODO: Informacje o portach i formacie pakietów
          </Typography>
          <Typography variant="body1">
            See the project <a href="https://github.com/cb1986ster/Scout/">README</a> on github for a full description of the demo project.
          </Typography>
        </Box>
      </SectionContent>
    )
  }

}

export default ScoutInformation;
