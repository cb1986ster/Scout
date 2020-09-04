import React, { Component } from 'react';
import { Redirect, Switch, RouteComponentProps } from 'react-router-dom'

import { Tabs, Tab } from '@material-ui/core';

import { PROJECT_PATH } from '../api';
import { MenuAppBar } from '../components';
import { AuthenticatedRoute } from '../authentication';

import ScoutInformation from './ScoutInformation';
// import LightStateRestController from './LightStateRestController';
// import LightStateWebSocketController from './LightStateWebSocketController';
import ScoutSettingsController from './ScoutSettingsController';

class Scout extends Component<RouteComponentProps> {

  handleTabChange = (event: React.ChangeEvent<{}>, path: string) => {
    this.props.history.push(path);
  };

  render() {
    return (
      <MenuAppBar sectionTitle="Scout Project">
        <Tabs value={this.props.match.url} onChange={this.handleTabChange} variant="fullWidth">
          <Tab value={`/${PROJECT_PATH}/scout/information`} label="Information" />
          {/* <Tab value={`/${PROJECT_PATH}/scout/rest`} label="REST Controller" /> */}
          {/* <Tab value={`/${PROJECT_PATH}/scout/socket`} label="WebSocket Controller" /> */}
          <Tab value={`/${PROJECT_PATH}/scout/settings`} label="Settings" />
        </Tabs>
        <Switch>
          <AuthenticatedRoute exact path={`/${PROJECT_PATH}/scout/information`} component={ScoutInformation} />
          {/* <AuthenticatedRoute exact path={`/${PROJECT_PATH}/scout/rest`} component={LightStateRestController} /> */}
          {/* <AuthenticatedRoute exact path={`/${PROJECT_PATH}/scout/socket`} component={LightStateWebSocketController} /> */}
          <AuthenticatedRoute exact path={`/${PROJECT_PATH}/scout/settings`} component={ScoutSettingsController} />
          <Redirect to={`/${PROJECT_PATH}/scout/information`} />
        </Switch>
      </MenuAppBar>
    )
  }

}

export default Scout;
