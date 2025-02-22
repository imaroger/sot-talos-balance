/*
 * Copyright 2018, Gepetto team, LAAS-CNRS
 *
 * This file is part of sot-talos-balance.
 * sot-talos-balance is free software: you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public License
 * as published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 * sot-talos-balance is distributed in the hope that it will be
 * useful, but WITHOUT ANY WARRANTY; without even the implied warranty
 * of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.  You should
 * have received a copy of the GNU Lesser General Public License along
 * with sot-talos-balance.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef __sot_talos_balance_qualisys_client_H__
#define __sot_talos_balance_qualisys_client_H__

/* --------------------------------------------------------------------- */
/* --- API ------------------------------------------------------------- */
/* --------------------------------------------------------------------- */

#if defined(WIN32)
#if defined(position_controller_EXPORTS)
#define QUALISYS_CLIENT_EXPORT __declspec(dllexport)
#else
#define QUALISYS_CLIENT_EXPORT __declspec(dllimport)
#endif
#else
#define QUALISYS_CLIENT_EXPORT
#endif

/* --------------------------------------------------------------------- */
/* --- INCLUDE --------------------------------------------------------- */
/* --------------------------------------------------------------------- */

#include <dynamic-graph/signal-helper.h>

#include <map>
#include "boost/assign.hpp"
#include <sot/core/robot-utils.hh>
#include <boost/thread.hpp>
#include <boost/chrono.hpp>

#include "sot/talos_balance/sdk_qualisys/RTProtocol.h"
#include "sot/talos_balance/sdk_qualisys/Markup.h"
#include "sot/talos_balance/sdk_qualisys/Network.h"
#include "sot/talos_balance/sdk_qualisys/RTPacket.h"

namespace dynamicgraph {
namespace sot {
namespace talos_balance {

/* --------------------------------------------------------------------- */
/* --- CLASS ----------------------------------------------------------- */
/* --------------------------------------------------------------------- */

class QUALISYS_CLIENT_EXPORT QualisysClient : public ::dynamicgraph::Entity {
  DYNAMIC_GRAPH_ENTITY_DECL();

 public:
  EIGEN_MAKE_ALIGNED_OPERATOR_NEW

  /* --- CONSTRUCTOR ---- */
  QualisysClient(const std::string& name);

  void init();

  /* --- SIGNALS --- */
  DECLARE_SIGNAL_IN(dummy, double);

  /* --- COMMANDS --- */
  void registerRigidBody(const std::string& RBname);
  void setMocapIPAdress(const std::string& ipAdress);
  void getRigidBodyList();  /// If connected, return the list of all the rigid bodies available.

  /* --- ENTITY INHERITANCE --- */
  virtual void display(std::ostream& os) const;

 protected:
  bool m_initSucceeded;  // true if the entity has been successfully initialized
  bool m_printRigidBodyList = false;
  std::vector<std::string> m_RBnames;     // vector of names of registered rigid bodies
  std::vector<dg::Vector> m_RBpositions;  // vector of rigid bodies positions
  void manageNetworkFrame();
  boost::thread m_thread{&QualisysClient::manageNetworkFrame, this};
  boost::mutex m_mutex;
  std::string m_serverAddr = "127.0.0.1";
  dg::Vector& readGenericRigidBody(const int RBidx, dg::Vector& res, const int& time);
};  // class QualisysClient

}  // namespace talos_balance
}  // namespace sot
}  // namespace dynamicgraph

#endif  // #ifndef __sot_talos_balance_qualisys_client_H__
