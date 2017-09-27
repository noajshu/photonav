import React, { Component } from 'react'
import { connect } from 'react-redux'
import PropTypes from 'prop-types'
import _ from 'lodash'
import { fetchPhotos } from '../actions'
// import NativeListener from 'react-native-listener';


import { movePhotoToRow, setCursor, moveCursor } from '../actions'

import { numRows, numPhotosInView } from '../reducers'

import '../style/style.scss'


const keymap = {
  PHOTO_NAVIGATOR: {
    MOVE_PHOTO_UP: 'up',
    MOVE_PHOTO_DOWN: 'down',
    MOVE_CURSOR_LEFT: ['command+left', 'left'],
    MOVE_CURSOR_RIGHT: ['command+right', 'right'],
    MOVE_CURSOR_UP: ['command+up', 'ctrl+up'],
    MOVE_CURSOR_DOWN: ['command+down', 'ctrl+down']
  },
}
import { ShortcutManager, Shortcuts } from 'react-shortcuts'
const shortcutManager = new ShortcutManager(keymap)


class Photo extends Component {
  render() {
    return _.range(numRows).map(
      j => <div className="container">{
        j == this.props.row ? <img src={this.props.src} /> : null
      }</div>
    )
  }
}

Photo = connect()

class PhotoNavigator extends Component {

  getChildContext() {
    return { shortcuts: shortcutManager }
  }

  // render() {
  //   return <div>
  //     {this.props.grid.rows.map(
  //       (row, i) => <div key={i}>
  //         row {i}: {row.map(
  //           (photo, j) => <img
  //             className={i == this.props.grid.cursor[0] && j == this.props.grid.cursor[1] ? 'selected' : ''}
  //             src={photo.url}
  //             key={j}
  //             onClick={e => this.props.selectPhoto(i, j)}
  //           />
  //         )}
  //       </div>
  //     )}
  //   </div>
  // }

  componentDidMount() {
    this.props.fetchPhotos()
  }

  _handleShortcuts = (action, event) => {
    switch (action) {
      case 'MOVE_PHOTO_UP':
        if(this.props.grid.photos[this.props.grid.cursor].row - 1 >= 0){
          this.props.movePhotoToRow(
            this.props.grid.cursor,
            this.props.grid.photos[this.props.grid.cursor].row - 1
          )
        }
        break
      case 'MOVE_PHOTO_DOWN':
        this.props.movePhotoToRow(
          this.props.grid.cursor,
          this.props.grid.photos[this.props.grid.cursor].row + 1
        )
        break
      case 'MOVE_CURSOR_LEFT':
        this.props.moveCursor('left')
        break
      case 'MOVE_CURSOR_RIGHT':
        this.props.moveCursor('right')
        break
      case 'MOVE_CURSOR_UP':
        this.props.moveCursor('up')
        break
      case 'MOVE_CURSOR_DOWN':
        this.props.moveCursor('down')
        break
    }
  }

  render() {
    if (this.props.grid === null) {
      return <div>Loading...</div>
    }

    return <Shortcuts name='PHOTO_NAVIGATOR' handler={this._handleShortcuts.bind(this)}>
      <div className="global-container">
        {/*
          _.range(numRows).map(
            j => (Math.abs(j - this.props.grid.cursor)) ? <div key={j} className="container">
              {this.props.grid.photos.map(
                (photo, i) => (
                  photo.row == j ? <div className="item" key={i}><img
                    className={i == this.props.grid.cursor ? 'selected' : ''}
                    src={photo.url}
                    onClick={e => this.props.setCursor(i)}
                  /></div> : <div className="item" key={i}><img /></div>
                )
              )}
            </div> : null
          )
        */}
        <div className="container">
        {
          _.range(3).map(
            // i => <Photo key={i} i={i}></Photo>
            i => <div key={i}>photo goes here</div>
          )
        }
        </div>
      </div>
    </Shortcuts>
  }
}

PhotoNavigator.childContextTypes = {
  shortcuts: PropTypes.object.isRequired
}

export default connect(
  state => ({
    grid: state.grid
  }),
  { setCursor, moveCursor, movePhotoToRow, fetchPhotos }
)(PhotoNavigator)
