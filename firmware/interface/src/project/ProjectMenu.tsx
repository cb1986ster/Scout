import React, { Component } from 'react';
import { Link, withRouter, RouteComponentProps } from 'react-router-dom';

import {List, ListItem, ListItemIcon, ListItemText} from '@material-ui/core';
import MemoryIcon from '@material-ui/icons/Memory';

import { PROJECT_PATH } from '../api';

class ProjectMenu extends Component<RouteComponentProps> {

  render() {
    const path = this.props.match.url;
    return (
      <List>
        <ListItem to={`/${PROJECT_PATH}/scout/`} selected={path.startsWith(`/${PROJECT_PATH}/scout/`)} button component={Link}>
          <ListItemIcon>
            <MemoryIcon />
          </ListItemIcon>
          <ListItemText primary="Scout" />
        </ListItem>
      </List>
    )
  }

}

export default withRouter(ProjectMenu);
