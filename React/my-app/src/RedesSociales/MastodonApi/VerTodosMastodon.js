// import React, { useState } from 'react';
// import { getAllMastodonData } from './mastodonApi';
// import { Spinner, Button, Form, DropdownButton, Dropdown } from 'react-bootstrap';
// import './VerTodosMastodon.css';

// const VerTodosMastodon = () => {
//   const [mastodonData, setMastodonData] = useState([]);
//   const [dataLoaded, setDataLoaded] = useState(false);
//   const [loading, setLoading] = useState(false);
//   const [filter, setFilter] = useState('');
//   const [dataType, setDataType] = useState('accounts'); // Default type

//   const fetchData = async (type) => {
//     setLoading(true);
//     try {
//       const data = await getAllMastodonData();
//       switch (type) {
//         case 'accounts':
//           setMastodonData(data.accounts || []);
//           break;
//         case 'statuses':
//           setMastodonData(data.statuses || []);
//           break;
//         case 'hashtags':
//           setMastodonData(data.hashtags || []);
//           break;
//         case 'all':
//         default:
//           setMastodonData([...data.accounts, ...data.statuses, ...data.hashtags]);
//           break;
//       }
//       setDataLoaded(true);
//     } catch (error) {
//       console.error('Failed to fetch Mastodon data:', error);
//     } finally {
//       setLoading(false);
//     }
//   };

//   const handleFilterChange = (event) => {
//     setFilter(event.target.value);
//   };

//   const handleTypeChange = (type) => {
//     setDataType(type);
//     fetchData(type);
//   };

//   const filteredData = mastodonData.filter(item =>
//     item.display_name?.toLowerCase().includes(filter.toLowerCase()) ||
//     item.username?.toLowerCase().includes(filter.toLowerCase()) ||
//     item.content?.toLowerCase().includes(filter.toLowerCase()) ||
//     item.name?.toLowerCase().includes(filter.toLowerCase())
//   );

//   return (
//     <div>
//       <h1>Mastodon Data</h1>
//       <div className="d-flex justify-content-between mb-3">
//         <DropdownButton id="dropdown-basic-button"  title={`View: ${dataType}`} onSelect={handleTypeChange}>
//           <Dropdown.Item eventKey="accounts">Accounts</Dropdown.Item>
//           <Dropdown.Item eventKey="statuses">Statuses</Dropdown.Item>
//           <Dropdown.Item eventKey="hashtags">Hashtags</Dropdown.Item>
//           <Dropdown.Item eventKey="all">All</Dropdown.Item>
//         </DropdownButton>
//         <Button className="btn btn-primary button-primary" onClick={() => fetchData(dataType)}>Load Mastodon Data</Button>
//       </div>
//       <Form.Control
//         type="text"
//         placeholder="Filter by name, username, content, or hashtag"
//         value={filter}
//         onChange={handleFilterChange}
//         className="mb-3"
//       />
//       {loading && <Spinner animation="border" />}
//       {dataLoaded && filteredData.length === 0 && <p>No data available</p>}
//       {dataLoaded && filteredData.length > 0 && (
//         <div>
//           {filteredData.map((item, index) => (
//             <div key={index} className="mastodon-item mb-3">
//               {item.avatar && <img src={item.avatar} alt={item.username} className="avatar" />}
//               {item.display_name && <h2>{item.display_name} ({item.username})</h2>}
//               {item.note && <p>{item.note}</p>}
//               {item.content && (
//                 <div className="status-content">
//                   <p><strong>Content:</strong> {item.content}</p>
//                   <p><strong>Created At:</strong> {new Date(item.created_at).toLocaleString()}</p>
//                   <p><strong>Language:</strong> {item.language}</p>
//                   <p><strong>Visibility:</strong> {item.visibility}</p>
//                   <p><strong>Replies:</strong> {item.replies_count}</p>
//                   <p><strong>Reblogs:</strong> {item.reblogs_count}</p>
//                   <p><strong>Favourites:</strong> {item.favourites_count}</p>
//                   <a href={item.url} target="_blank" rel="noopener noreferrer">View on Mastodon</a>
//                 </div>
//               )}
//               {item.name && <h2>#{item.name}</h2>}
//               {item.url && (
//                 <a href={item.url} target="_blank" rel="noopener noreferrer">
//                   Profile Link
//                 </a>
//               )}
//             </div>
//           ))}
//         </div>
//       )}
//     </div>
//   );
// };

// export default VerTodosMastodon;
